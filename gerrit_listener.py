#!/usr/bin/python
import os
import notify
import requests
import time
import json

class Gerrit_Snapshot(object):
  GERRIT_API = 'http://sscssepx2:8081/changes/?o=LABELS'
  GERRIT_ICON = os.path.dirname(os.path.realpath(__file__)) + '/gerrit.png'

  time = None
  content = None
  queue = None
  changed = False
  
  def __init__(self, time):
    self.time = time
    self.data = None
    self.content = ''.join(requests.get(self.GERRIT_API).text.splitlines(True)[1:])
    return  
  
  def update(self):
    self.content = ''.join(requests.get(self.GERRIT_API).text.splitlines(True)[1:])
    
  def report(self, start):
    self.data = json.loads(self.content)
    notification = ""
    for patchset in self.data:
      if (patchset['mergeable']):
        notification = notification + patchset["subject"] + " is mergeable.\n"
    if start:
      notification = notification + "There are %d open patch sets" % len(self.data)
    if notification != "":
      notify.notify(summary = "Gerrit notifcation", body = notification, app_icon=self.GERRIT_ICON)
    return 

if __name__ == "__main__":
  snapshot = Gerrit_Snapshot(int (time.time()))  
  snapshot.report(start=True)
  while True:
    time.sleep(300)
    snapshot.update()
    snapshot.report(start=False)

