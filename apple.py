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
import re

from bs4 import BeautifulSoup

class Apple_Snapshot(object):
  Apple_API = 'http://hkm.appledaily.com/list.php?category=instant'
  AppleDetail_API = 'http://hkm.appledaily.com/'
  Apple_Cat = {'要聞' : '6996647', '突發' : '10829391', '兩岸' : '10793096', '國際' : '10793140'}
  Apple_File = {'要聞' : 'main', '突發' : 'new', '兩岸' : 'ch', '國際' : 'int'}
  
  Apple_ICON = os.path.dirname(os.path.realpath(__file__)) + '/svd.jpg'
  DIR = os.environ['HOME'] + '/Downloads/hknews'
  time = None
  content = None
  queue = None
  changed = False
  
  def __init__(self, time):
    self.time = time
    self.content = {'要聞' : [], '突發' : [], '兩岸' : [], '國際' : []}
    self.get_contents();
    return  
  
  def get_contents(self):
    for key in self.Apple_Cat:
      r = requests.get(self.Apple_API + "&category_guid=" + self.Apple_Cat[key])
      r.encoding = 'utf-8'
      self.content[key] = self.digest(r.text)
  
  def digest(self, raw_content):
    content = []
    soup = BeautifulSoup(raw_content)
    all_div = soup.findAll("div", "content-list clearfix")[0].findAll("a")
    for div in all_div:
      article = {"title" : "", "friendlyDateShort" : "", "url" : "", "date" : ""}
      article["url"] = div['href']
      article["title"] = div.find('p').text
      article["friendlyDateShort"] = div.find('label').text
      content.append(article)
    return content
  
  def report_start(self):
    notification = ""
    for article in self.content['突發'][0:7]:
      notification = notification  + article["title"] + "\n"
      output=self.format_results(article)
    for key in self.Apple_Cat:
      content = self.content[key]
      for article in reversed(content):
        output=self.format_results(article)
        self.send_to_file(output, self.Apple_File[key])
    notify.notify(summary = "Apple listener is started", body = notification, app_icon=self.Apple_ICON, timeout=15000)
    return 

  def report_difference(self, last_snapshot):
    for key in self.Apple_Cat:
      content = self.content[key]
      for article in reversed(content):
        current_changed = True
        for last_article in last_snapshot.content[key]:
          if article["title"] == last_article["title"]:
            current_changed = False
        if current_changed:
          notify.notify(summary = article["title"], app_icon=self.Apple_ICON, timeout=15000)
          output=self.format_results(article)
          self.send_to_file(output, self.Apple_File[key])
    return 
  
  def format_results(self, article):
    """Extract the results from a wiki XML content
    """  
    output = "\n" 
    fulltext = requests.get(self.AppleDetail_API + article["url"])
    fulltext.encoding = 'utf-8'
    soup = BeautifulSoup(fulltext.text)
    article["date"] = soup.findAll("p","text lastupdate")[0].text
    output = output + '<b>%-23s' % article["date"] + article["title"] + "</b>\n\n"
    alltext = soup.findAll("p","text")
    alltext.pop(0)
    alltext.pop(0)
    
    for text in alltext:
      output = output + text.get_text() + "\n\n"
    output = output + "<tt>Source: " + self.AppleDetail_API + article["url"]  + "</tt>\n"
    output = common.format_color(output).encode('utf-8')
    return output

  def send_to_file(self, output, key):
    filename = self.DIR + '/' + key + '-'+ time.strftime("%Y%m%d")
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
    time.sleep(360)
    snapshot = Apple_Snapshot(int (time.time()))
    snapshot.report_difference(old_snapshot)
    old_snapshot = snapshot

