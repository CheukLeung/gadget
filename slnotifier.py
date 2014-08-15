#!/usr/bin/python
import sl
import Tkinter
import time
import os
from PIL import Image, ImageTk


root = Tkinter.Tk()
sl_icon = os.path.dirname(os.path.realpath(__file__)) + '/sl.png'
image = Image.open(sl_icon)
photo = ImageTk.PhotoImage(image)

sl_ins = sl.SL("4634", "2")
sl_ins.get_results()
traffics = sl_ins.traffics
blue = '#2A9CD5'
white = '#FFFFFF'
grey = '#CCCCCC'

Tkinter.Label(root, image=photo, bg=blue, anchor=Tkinter.W).grid(ipadx=5, row=0, column=0, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
Tkinter.Label(root, text=sl_ins.idname, bg=blue, fg=white, font=('Helvetica', 18, 'bold')).grid(ipadx=5, row=0, column=1, columnspan=3, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)

r=1
Tkinter.Label(root, text="Type", bg=blue, fg=white, anchor=Tkinter.W).grid(ipadx=5, row=r, column=0, sticky=Tkinter.E+Tkinter.W)
Tkinter.Label(root, text="Line", bg=blue, fg=white, anchor=Tkinter.W).grid(ipadx=5, row=r, column=1, sticky=Tkinter.E+Tkinter.W)
Tkinter.Label(root, text="Destination", bg=blue, fg=white, anchor=Tkinter.W).grid(ipadx=5, row=r, column=2, sticky=Tkinter.E+Tkinter.W)
Tkinter.Label(root, text="Time", bg=blue, fg=white, anchor=Tkinter.W).grid(ipadx=5, row=r, column=3, sticky=Tkinter.E+Tkinter.W)
r=r+1
for traffic in traffics:
  if r % 2:
    bg = grey
  else:
    bg = white
  Tkinter.Label(root, text=traffic['TransportMode'], bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=0, sticky=Tkinter.E+Tkinter.W)
  Tkinter.Label(root, text=traffic['LineNumber'], bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=1, sticky=Tkinter.E+Tkinter.W)
  Tkinter.Label(root, text=traffic['Destination'], bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=2, sticky=Tkinter.E+Tkinter.W)
  Tkinter.Label(root, text=traffic['DisplayTime'], bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=3, sticky=Tkinter.E+Tkinter.W)
  r=r+1

Tkinter.Label(root, text=sl_ins.time, bg=blue, fg=white, anchor=Tkinter.E).grid(ipadx=5, row=r, columnspan=4, sticky=Tkinter.E+Tkinter.W)

root.mainloop()
