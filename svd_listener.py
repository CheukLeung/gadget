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
  SvD_API = 'http://www.svd.se/search.do?output=json&section1=Nyheter'
  SvD_ICON = os.path.dirname(os.path.realpath(__file__)) + '/svd.jpg'
  DIR = os.environ['HOME'] + '/Downloads/news'
  time = None
  content = None
  queue = None
  changed = False
  
  def __init__(self, time):
    self.time = time
    self.content = requests.get(self.SvD_API + "&%d" % random.randint(1, 9999999)).json()["SvDSearch"]["results"]["articles"]
    return  

  def report_start(self):
    notification = ""
    for article in reversed(self.content[0:7]):
      notification = notification  + article["title"] + "\n"
      output=self.format_results(article)
      self.send_to_file(output)
    notify.notify(summary = "SvD listener is started", body = notification, app_icon=self.SvD_ICON, timeout=10000)
    return 

  def report_difference(self, last_snapshot):
    for article in reversed(self.content):
      current_changed = True
      for last_article in last_snapshot.content: 
        if article["title"] == last_article["title"] and article["friendlyDateShort"] == last_article["friendlyDateShort"]:   
          current_changed = False
      if current_changed:
        notify.notify(summary = article["title"], body = article["description"] + " (" + article["friendlyDateShort"] + ")\n" , app_icon=self.SvD_ICON, timeout=10000)
        output=self.format_results(article)
        self.send_to_file(output)
    return 
  
  def format_results(self, article):
    """Extract the results from a wiki XML content
    """  
    output = "\n" 
    output = output + '<b>%-15s' % article["friendlyDateShort"] + article["title"] + "</b>\n"
    output = output + '<code>' + article["description"] + "</code>\n"
    fulltext = requests.get(article["url"])
    soup = BeautifulSoup(fulltext.text)
    [s.extract() for s in soup('script')]
    all_div = soup.findAll("div","articletext")
    if len(all_div) > 0:
      output = output + all_div[0].get_text().replace("\n\n", "\n")
      
    output = output + "<tt>Source: " + article["url"]  + "</tt>\n"
    output = common.format_color(output).encode('utf-8')
    return output

  def send_to_file(self, output):
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
    time.sleep(60)
    snapshot = SvD_Snapshot(int (time.time()))
    snapshot.report_difference(old_snapshot)
    old_snapshot = snapshot

