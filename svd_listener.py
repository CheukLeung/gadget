#!/usr/bin/python
import os
import notify
import requests
import time
import random
import requests
import common
import util
from bs4 import BeautifulSoup

class SvD_Snapshot(object):
  SvD_API = 'http://rss2json.com/api.json?rss_url=http://www.svd.se/?service=rss'
  SvD_ICON = os.path.dirname(os.path.realpath(__file__)) + '/svd.jpg'
  DIR = os.environ['HOME'] + '/.news'
  time = None
  content = None
  queue = None
  changed = False

  def __init__(self, time):
    self.time = time
    self.content = requests.get(self.SvD_API).json()["items"]
    return

  def report_start(self):
    notification = ""
    for article in reversed(self.content[0:7]):
      notification = notification  + article["title"] + "\n"
      output=self.format_results(article)
      self.send_to_file(output)
    return

  def report_difference(self, last_snapshot):
    for article in reversed(self.content):
      current_changed = True
      for last_article in last_snapshot.content:
        if article["guid"] == last_article["guid"]:
          current_changed = False
      if current_changed:
        output=self.format_results(article)
        self.send_to_file(output)
    return

  def format_results(self, article):
    """Extract the results from a wiki XML content
    """
    output = "\n"
    output = output + "<b>" + article["title"] + "</b>\n"
    output = output + '%-15s' % article["pubDate"] + "\n"
    output = output + '<i>' + article["description"] + "</i>\n"
    fulltext = requests.get(article["link"])
    soup = BeautifulSoup(fulltext.text)
    [s.extract() for s in soup('script')]

    all_div = soup.findAll(itemprop="articleBody")[0]
    for div in all_div.findAll("figure"):
      div.decompose()
    for div in all_div.findAll("div"):
      div.decompose()
    if len(all_div) > 0:
      output = output + all_div.get_text().replace("\n\n", "\n")

    output = output + "<tt>Source: " + article["link"]  + "</tt>\n"
    output = common.format_color(output).encode('utf-8')
    output = common.remove_html_code(output)
    return output

  def send_to_file(self, output):
    print output
    filename = self.DIR + '/news-' + time.strftime("%Y%m%d")
    if os.path.exists(filename):
      f = file(filename, "r+")
      content = output + '\n' + f.read()
      f.close()
    else:
      content = output
    f = file(filename, "w")
    f.write(content)
    f.close()

if __name__ == "__main__":
  snapshot = SvD_Snapshot(int (time.time()))
  snapshot.report_start()
  old_snapshot = snapshot
  while True:
    time.sleep(360)
    snapshot = SvD_Snapshot(int (time.time()))
    snapshot.report_difference(old_snapshot)
    old_snapshot = snapshot
