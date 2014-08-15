#!/usr/bin/python
import sl
from Tkinter import *
import time
import os
from PIL import Image, ImageTk
import csv

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
    self.direction = 2
    self.f=Frame()
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
    self.siteid = self.data[index]['SiteId']
    self.selector.destroy()
    self.draw()
  

  def selector_callback(self):
    self.selector = Tk()
    self.selector.wm_title("Select a place")
    self.selector.geometry("250x700")
    r=0
    blue = '#2A9CD5'
    white = '#FFFFFF'
    grey = '#CCCCCC'
    listbox = Listbox(self.selector, selectmode=SINGLE)
    listbox.bind("<Double-Button-1>", self.change_id)
    listbox.pack(fill=BOTH, expand=1)
    for stop in self.data:
      if r % 2:
        bg = grey
      else:
        bg = white
      listbox.insert(END, stop['SiteName'])
      
      r=r+1    
    self.selector.mainloop()

  def update_clock(self):
    self.draw()
    self.root.after(20000, self.update_clock)

  def draw(self):
    self.f.grid_forget()
    self.f.destroy()
    self.f=Frame()
    self.f.pack()
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
    
    index = next(index for (index, d) in enumerate(self.data) if d["SiteId"] == self.siteid)
 
    Label(self.f, bd=0, image=self.photo, bg=blue, anchor=W).grid(ipadx=5, row=0, rowspan=2, column=0, sticky=E+W+N+S)
    Button(self.f, text=self.data[index]["SiteName"], font=('Helvetica', 18, 'bold'), bg=blue, fg=white, activeforeground=blue, highlightbackground=blue, activebackground=blue, relief=FLAT, highlightthickness=0, command=self.selector_callback).grid(ipadx=5, row=0, rowspan=2, column=1, columnspan=2, sticky=E+W+N+S)
    
    Button(self.f, image=self.refresh_photo, bg=blue, fg=blue, activeforeground=blue,  activebackground=blue, relief=FLAT, highlightthickness=0, highlightbackground=blue, command=self.update_callback).grid(ipadx=5, row=0, column=3, sticky=E+W+N+S)
    Button(self.f, image=direction_photo, bg=blue, fg=blue, activeforeground=blue,  activebackground=blue, relief=FLAT, highlightthickness=0, highlightbackground=blue, command=self.reverse_callback).grid(ipadx=5, row=1, column=3, sticky=E+W+N+S)
    
    r=2
    Label(self.f, text="Type", bg=blue, fg=white, anchor=W).grid(ipadx=5, row=r, column=0, sticky=E+W)
    Label(self.f, text="Line", bg=blue, fg=white, anchor=W).grid(ipadx=5, row=r, column=1, sticky=E+W)
    Label(self.f, text="Destination", bg=blue, fg=white, anchor=W).grid(ipadx=5, row=r, column=2, sticky=E+W)
    Label(self.f, text="Time", bg=blue, fg=white, anchor=W).grid(ipadx=5, row=r, column=3, sticky=E+W)
    r=r+1
    for traffic in traffics:
      if r % 2:
        bg = grey
      else:
        bg = white
      Label(self.f, text=traffic['TransportMode'], bg=bg, anchor=W).grid(ipadx=5, row=r, column=0, sticky=E+W)
      Label(self.f, text=traffic['LineNumber'], bg=bg, anchor=W).grid(ipadx=5, row=r, column=1, sticky=E+W)
      Label(self.f, text=traffic['Destination'], bg=bg, anchor=W).grid(ipadx=5, row=r, column=2, sticky=E+W)
      Label(self.f, text=traffic['DisplayTime'], bg=bg, anchor=W).grid(ipadx=5, row=r, column=3, sticky=E+W)
      r=r+1

    Label(self.f, text=sl_ins.time, bg=blue, fg=white, anchor=E).grid(ipadx=5, row=r, columnspan=4, sticky=E+W)


app=App()
