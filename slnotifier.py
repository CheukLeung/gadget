#!/usr/bin/python
import sl
import Tkinter
import time
import os
from PIL import Image, ImageTk



class App():
  
  sl_icon = os.path.dirname(os.path.realpath(__file__)) + '/sl.png'
  to_icon = os.path.dirname(os.path.realpath(__file__)) + '/front.png'
  back_icon = os.path.dirname(os.path.realpath(__file__)) + '/back.png'
  refresh_icon = os.path.dirname(os.path.realpath(__file__)) + '/refresh.png'
  
  def __init__(self):
    self.root = Tkinter.Tk()
    image = Image.open(self.sl_icon)
    self.photo = ImageTk.PhotoImage(image)
    image = Image.open(self.to_icon)
    self.to_photo = ImageTk.PhotoImage(image)
    image = Image.open(self.back_icon)
    self.back_photo = ImageTk.PhotoImage(image)
    image = Image.open(self.refresh_icon)
    self.refresh_photo = ImageTk.PhotoImage(image)
    
    self.direction = 2
    self.update_clock()
    self.root.mainloop()


  def update_callback(self):
    self.draw()

  def reverse_callback(self):
    self.direction = self.direction % 2 + 1
    self.draw()

  def update_clock(self):
    self.draw()
    self.root.after(20000, self.update_clock)

  def draw(self):
    sl_ins = sl.SL("4634", "%d" % self.direction)
    sl_ins.get_results()
    if self.direction % 2:
      direction_photo = self.back_photo
    else:
      direction_photo = self.to_photo
      
    traffics = sl_ins.traffics
    blue = '#2A9CD5'
    white = '#FFFFFF'
    grey = '#CCCCCC'
 
    Tkinter.Label(self.root, bd=0, image=self.photo, bg=blue, anchor=Tkinter.W).grid(ipadx=5, row=0, rowspan=2, column=0, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
    Tkinter.Label(self.root, text=sl_ins.idname, bg=blue, fg=white, font=('Helvetica', 18, 'bold')).grid(ipadx=5, row=0, rowspan=2, column=1, columnspan=2, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
    Tkinter.Button(self.root, image=self.refresh_photo, bg=blue, fg=blue, activeforeground=blue,  activebackground=blue, relief=Tkinter.FLAT, highlightcolor=blue, highlightbackground=blue, highlightthickness=0, command=self.update_callback).grid(ipadx=5, row=0, column=3, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
    Tkinter.Button(self.root, image=direction_photo, bg=blue, fg=blue, activeforeground=blue,  activebackground=blue, relief=Tkinter.FLAT, highlightcolor=blue, highlightbackground=blue, highlightthickness=0, command=self.reverse_callback).grid(ipadx=5, row=1, column=3, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
    
    r=2
    Tkinter.Label(self.root, text="Type", bg=blue, fg=white, anchor=Tkinter.W).grid(ipadx=5, row=r, column=0, sticky=Tkinter.E+Tkinter.W)
    Tkinter.Label(self.root, text="Line", bg=blue, fg=white, anchor=Tkinter.W).grid(ipadx=5, row=r, column=1, sticky=Tkinter.E+Tkinter.W)
    Tkinter.Label(self.root, text="Destination", bg=blue, fg=white, anchor=Tkinter.W).grid(ipadx=5, row=r, column=2, sticky=Tkinter.E+Tkinter.W)
    Tkinter.Label(self.root, text="Time", bg=blue, fg=white, anchor=Tkinter.W).grid(ipadx=5, row=r, column=3, sticky=Tkinter.E+Tkinter.W)
    r=r+1
    for traffic in traffics:
      if r % 2:
        bg = grey
      else:
        bg = white
      Tkinter.Label(self.root, text=traffic['TransportMode'], bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=0, sticky=Tkinter.E+Tkinter.W)
      Tkinter.Label(self.root, text=traffic['LineNumber'], bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=1, sticky=Tkinter.E+Tkinter.W)
      Tkinter.Label(self.root, text=traffic['Destination'], bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=2, sticky=Tkinter.E+Tkinter.W)
      Tkinter.Label(self.root, text=traffic['DisplayTime'], bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=3, sticky=Tkinter.E+Tkinter.W)
      r=r+1

    Tkinter.Label(self.root, text=sl_ins.time, bg=blue, fg=white, anchor=Tkinter.E).grid(ipadx=5, row=r, columnspan=4, sticky=Tkinter.E+Tkinter.W)


app=App()
