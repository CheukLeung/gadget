#!/usr/bin/python
# -*- coding: utf-8 -*-

import sl
from Tkinter import *
import time
import os
from PIL import Image, ImageTk
import csv
import string
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class App():
  
  sl_icon = os.path.dirname(os.path.realpath(__file__)) + '/sl.png'
  to_icon = os.path.dirname(os.path.realpath(__file__)) + '/front.png'
  back_icon = os.path.dirname(os.path.realpath(__file__)) + '/back.png'
  refresh_icon = os.path.dirname(os.path.realpath(__file__)) + '/refresh.png'
  database = os.path.dirname(os.path.realpath(__file__)) + '/sites.csv'
  
  def __init__(self):
    self.root = Tk()
    self.root.wm_title("SL Realtime")
    self.siteid = "4634"
    image = Image.open(self.sl_icon)
    self.photo = ImageTk.PhotoImage(image)
    image = Image.open(self.to_icon)
    self.to_photo = ImageTk.PhotoImage(image)
    image = Image.open(self.back_icon)
    self.back_photo = ImageTk.PhotoImage(image)
    image = Image.open(self.refresh_icon)
    self.refresh_photo = ImageTk.PhotoImage(image)
    self.data = self.read_database()
    self.current_data = self.data
    self.direction = 2
    self.search_str = ""
    self.f=Frame()
    self.s=Frame()
    self.entry=None
    self.f.pack()
    self.selector = None
    self.update_clock()
    self.root.mainloop()
    
  def read_database(self):
    with open(self.database, 'Ur') as f:
      raw_data = list({'SiteId' : j, 'SiteName' : k, 'StopAreaNumber' : l, 'LastModifiedUtcDateTime' : m, 'ExistsFromDate' : n } for j, k, l, m, n in csv.reader(f, delimiter=';'))
    raw_data.pop(0)
    data = []
    last = {'SiteId' : 0, 'SiteName' : "" }
    for raw_point in raw_data:
      if last['SiteId'] != raw_point['SiteId'] or last['SiteName'] != raw_point['SiteName']:
        data.append(raw_point)
      last['SiteId'] = raw_point['SiteId']
      last['SiteName'] = raw_point['SiteName']
    return data

  def update_callback(self):
    self.draw()

  def reverse_callback(self):
    self.direction = self.direction % 2 + 1
    self.draw()
  
  def change_id(self, event):
    selector = event.widget
    index = int(selector.curselection()[0])
    self.siteid = self.current_data[index]['SiteId']
    self.selector.destroy()
    self.draw()
  
  def search(self, event):
    self.current_data = []
    if event.keycode == 3342463:
      target_name = event.widget.get()[:len(event.widget.get())-1]
    elif event.char in string.printable:
      target_name = event.widget.get()+event.char
    else:
      target_name = event.widget.get()
    self.search_str = target_name
    target_name = target_name.decode('utf-8').strip().lower().replace(' ', '')
    target_name = target_name.replace('ö', 'o')
    target_name = target_name.replace('ä', 'a')
    target_name = target_name.replace('å', 'a')
    target_name = target_name.replace('é', 'e')
    for stop in self.data:
      current_name = stop['SiteName'].decode('utf-8').strip().lower().replace(' ', '')
      current_name = current_name.replace('ö', 'o')
      current_name = current_name.replace('ä', 'a')
      current_name = current_name.replace('ä', 'a')
      current_name = current_name.replace('é', 'e')
      if target_name in current_name:
        self.current_data.append(stop)
    self.selector_draw()

  def selector_draw(self):
    r=0
    blue = '#2A9CD5'
    white = '#FFFFFF'
    grey = '#CCCCCC'
    self.s.pack_forget()
    self.s.destroy()
    self.s=Frame(self.selector)
    self.s.pack(fill=BOTH, expand=1)
    listbox = Listbox(self.s, selectmode=SINGLE)
    listbox.bind("<Double-Button-1>", self.change_id)
    listbox.pack(fill=BOTH, expand=1)
     
    for stop in self.current_data:
      if r % 2:
        bg = white
      else:
        bg = grey
      listbox.insert(END, stop['SiteName'])
      
      r=r+1

  def selector_callback(self):
    self.selector = Tk()
    self.selector.wm_title("Select a place")
    self.selector.geometry("250x700")
    self.s=Frame(self.selector)
    self.s.pack(fill=BOTH, expand=1)
    v = StringVar()

    self.entry = Entry(self.selector, bd=0, textvariable=v)
    v.set(self.search_str)
    self.entry.pack(fill=X)
    self.entry.bind("<Key>", self.search)
    self.entry.focus()
    self.selector_draw()
    self.selector.mainloop()

  def update_clock(self):
    self.draw()
    self.root.after(20000, self.update_clock)

  def draw(self):
    sl_ins = sl.SL(self.siteid, "%d" % self.direction)
    sl_ins.get_results()
    if self.direction % 2:
      direction_photo = self.back_photo
    else:
      direction_photo = self.to_photo
      
    traffics = sl_ins.traffics
    blue = '#2A9CD5'
    white = '#FFFFFF'
    grey = '#CCCCCC'
    f=Frame()
    index = next(index for (index, d) in enumerate(self.data) if d["SiteId"] == self.siteid)
 
    Label(f, bd=0, image=self.photo, bg=blue, anchor=W).grid(ipadx=5, row=0, rowspan=2, column=0, sticky=E+W+N+S)
    Button(f, text=self.data[index]["SiteName"], font=('Helvetica', 18, 'bold'), bg=blue, fg=white, activeforeground=white, highlightbackground=blue, activebackground=blue, relief=FLAT, highlightthickness=0, command=self.selector_callback).grid(ipadx=5, row=0, rowspan=2, column=1, columnspan=2, sticky=E+W+N+S)
    
    Button(f, image=self.refresh_photo, bg=blue, fg=blue, activeforeground=blue,  activebackground=blue, relief=FLAT, highlightthickness=0, highlightbackground=blue, command=self.update_callback).grid(ipadx=5, row=0, column=3, sticky=E+W+N+S)
    Button(f, image=direction_photo, bg=blue, fg=blue, activeforeground=blue,  activebackground=blue, relief=FLAT, highlightthickness=0, highlightbackground=blue, command=self.reverse_callback).grid(ipadx=5, row=1, column=3, sticky=E+W+N+S)
    
    r=2
    Label(f, text="Type", bg=blue, fg=white, anchor=W).grid(ipadx=5, row=r, column=0, sticky=E+W)
    Label(f, text="Line", bg=blue, fg=white, anchor=W).grid(ipadx=5, row=r, column=1, sticky=E+W)
    Label(f, text="Destination", bg=blue, fg=white, anchor=W).grid(ipadx=5, row=r, column=2, sticky=E+W)
    Label(f, text="Time", bg=blue, fg=white, anchor=W).grid(ipadx=5, row=r, column=3, sticky=E+W)
    r=r+1
    for traffic in traffics:
      if r % 2:
        bg = white
      else:
        bg = grey
      Label(f, text=traffic['TransportMode'], bg=bg, anchor=W).grid(ipadx=5, row=r, column=0, sticky=E+W)
      Label(f, text=traffic['LineNumber'], bg=bg, anchor=W).grid(ipadx=5, row=r, column=1, sticky=E+W)
      Label(f, text=traffic['Destination'], bg=bg, anchor=W).grid(ipadx=5, row=r, column=2, sticky=E+W)
      Label(f, text=traffic['DisplayTime'], bg=bg, anchor=W).grid(ipadx=5, row=r, column=3, sticky=E+W)
      r=r+1

    Label(f, text=sl_ins.time, bg=blue, fg=white, anchor=E).grid(ipadx=5, row=r, columnspan=4, sticky=E+W)

    self.f.grid_forget()
    self.f.destroy()
    self.f=f
    self.f.pack()

app=App()
