#!/usr/bin/python
import os
import notify
import requests
import time
import random

class SvD_Snapshot(object):
  SvD_API = 'http://www.svd.se/search.do?output=json&section1=Nyheter'
  SvD_ICON = os.path.dirname(os.path.realpath(__file__)) + '/svd.jpg'

  time = None
  content = None
  queue = None
  changed = False
  
  def __init__(self, time):
    self.time = time
    self.content = requests.get(self.SvD_API + "&%d" % random.randint(1, 9999999)).json()["SvDSearch"]["results"]["articles"][0:7]
    return  

  def report_start(self):
    notification = ""
    for article in self.content:
      notification = notification  + article["title"] + "\n"
    notify.notify(summary = "SvD listener is started", body = notification, app_icon=self.SvD_ICON, timeout=10000)
    return 

  def report_difference(self, last_snapshot):
    jobs_count = len(self.content)
    for job in self.content:
      current_changed = True
      for last_job in last_snapshot.content: 
        if job["title"] == last_job["title"]:   
          jobs_count = jobs_count - 1
          current_changed = False
      if current_changed:
        notify.notify(summary = job["title"], body = job["description"] + " (" + article["friendlyDateShort"] + ")\n" , app_icon=self.SvD_ICON, timeout=10000)
    return 

      
if __name__ == "__main__":
  snapshot = SvD_Snapshot(int (time.time()))  
  snapshot.report_start()
  old_snapshot = snapshot
  while True:
    time.sleep(60)
    snapshot = SvD_Snapshot(int (time.time()))
    snapshot.report_difference(old_snapshot)
    old_snapshot = snapshot

