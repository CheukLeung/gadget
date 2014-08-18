#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import notify
import requests
import time
import random
import requests
import common
import util
from bs4 import BeautifulSoup

class Apple_Snapshot(object):
  Apple_API = 'http://hkm.appledaily.com/list.php?category=instant'
  Apple_Cat = {'要聞' : '6996647', '突發' : '10829391', '兩岸' : '10793096', '國際' : '10793140'}
  Apple_ICON = os.path.dirname(os.path.realpath(__file__)) + '/svd.jpg'
  DIR = os.environ['HOME'] + '/Downloads/hknews'
  time = None
  content = None
  queue = None
  changed = False
  
  def __init__(self, time):
    self.time = time
    self.content = {'要聞' : [1], '突發' : [2], '兩岸' : [3], '國際' : [5]}
    self.get_contents();
#    self.content = requests.get(self.SvD_API + "&%d" % random.randint(1, 9999999)).json()["SvDSearch"]["results"]["articles"]
    return  
  
  def get_contents(self):
    for key in self.Apple_Cat:
      self.content[key] = self.digest(requests.get(self.Apple_API + "&category_guid=" + self.Apple_Cat[key]).text)
  
  def digest(self, raw_content):
    soup = BeautifulSoup(raw_content)
    all_div = soup.findAll("p")
    if len(all_div) > 0:
      print all_div[0].get_text().encode('utf-8')
    return None
  #output = output + all_div[0].get_text().replace("\n\n", "\n")
  
  def report_start(self):
    notification = ""
    for article in reversed(self.content[0:7]):
      notification = notification  + article["title"] + "\n"
      output=self.format_results(article)
      self.send_to_file(output)
    notify.notify(summary = "SvD listener is started", body = notification, app_icon=self.SvD_ICON, timeout=15000)
    return 

  def report_difference(self, last_snapshot):
    for article in reversed(self.content):
      current_changed = True
      for last_article in last_snapshot.content: 
        if article["title"] == last_article["title"] and article["date"] == last_article["date"]:   
          current_changed = False
      if current_changed:
        notify.notify(summary = article["title"], body = article["description"] + " (" + article["friendlyDateShort"] + ")\n" , app_icon=self.SvD_ICON, timeout=15000)
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
    filename = self.DIR + '/hknews-' + time.strftime("%Y%m%d")
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
  snapshot = Apple_Snapshot(int (time.time()))  
  snapshot.report_start()
  old_snapshot = snapshot
  while True:
    time.sleep(60)
    snapshot = SvD_Snapshot(int (time.time()))
    snapshot.report_difference(old_snapshot)
    old_snapshot = snapshot

