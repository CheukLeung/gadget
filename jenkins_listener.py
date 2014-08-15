#!/usr/bin/python
import os
import notify
import requests
import time

class Jenkins_Snapshot(object):
  JENKINS_API = 'http://tmgsseco01:8080/api/json'
  JENKINS_QUEUE_API = 'http://tmgsseco01:8080/queue/api/json'
  JENKINS_ICON = os.path.dirname(os.path.realpath(__file__)) + '/jenkins.png'

  time = None
  content = None
  queue = None
  changed = False
  
  def __init__(self, time):
    self.time = time
    self.content = requests.get(self.JENKINS_API).json()["jobs"]
    self.queue = requests.get(self.JENKINS_QUEUE_API).json()["items"]
    return  

  def report_start(self):
    notification = ""
    for job in self.content:
      if "anime" in job["color"]:
        notification = notification + job["name"] + " is running.\n"
    notification = notification + "Jobs queue: %d" % len(self.queue)
    notify.notify(summary = "Jenkins listener is started", body = notification, app_icon=self.JENKINS_ICON)
    return 

  def report_difference(self, last_snapshot):
    notification = ""
    notification = notification + self.get_jobs_changed(last_snapshot)
    notification = notification + self.new_jobs(last_snapshot)
    notification = notification + "Jobs queue: %d" % len(self.queue)
    if self.changed:
      notify.notify(summary = "Jenkins jobs notifcation", body = notification, app_icon=self.JENKINS_ICON)
    return 
  
  def get_jobs_changed(self, last_snapshot):
    jobs_names = ""
    jobs_count = 0
    for job in self.content:
      for last_job in last_snapshot.content:
        if job["name"] == last_job["name"]:
          if job["color"] != last_job["color"]:
            self.changed = True
            jobs_names = jobs_names + job["name"] + self.resolve_text(job["color"] + "\n") 
      if "anime" in job["color"]:
        jobs_count = jobs_count + 1
    jobs_names = jobs_names + "Jobs running: %d\n" % jobs_count
    return jobs_names
  
  def new_jobs(self, last_snapshot):
    jobs_count = len(self.queue)
    for job in self.queue:
      for last_job in last_snapshot.queue: 
        if job["task"]["name"] == last_job["task"]["name"]:   
          jobs_count = jobs_count - 1    
    if jobs_count > 0:
      self.changed = True 
      return "%d new jobs are added in the queue.\n" % jobs_count
    else:
      return ""
  
  def resolve_text(self, text):
    resolved_text = ""
    if "anime" in text:
      resolved_text = " is started.\n"
    elif "red" in text:
      resolved_text = " failed.\n"
    elif "yellow" in text:
      resolved_text = " is finished with unstable.\n"
    elif "blue" in text:
      resolved_text = " is finished successfully.\n"
    elif "aborted" in text:
      resolved_text = " is aborted.\n"
    return resolved_text 
      
if __name__ == "__main__":
  snapshot = Jenkins_Snapshot(int (time.time()))  
  snapshot.report_start()
  old_snapshot = snapshot
  while True:
    time.sleep(30)
    snapshot = Jenkins_Snapshot(int (time.time()))
    snapshot.report_difference(old_snapshot)
    old_snapshot = snapshot

