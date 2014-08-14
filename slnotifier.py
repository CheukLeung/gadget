#!/usr/bin/python
import sl
import Tkinter
import time
root = Tkinter.Tk()

sl_ins = sl.SL("4634", "2")
sl_ins.get_results()
traffics = sl_ins.traffics
r=1
Tkinter.Label(root, text="Type", bd=1, bg='#0089FF', fg='#FFFFFF', anchor=Tkinter.W).grid(ipadx=5, row=0, column=0, sticky=Tkinter.W)
Tkinter.Label(root, text="Type", bd=1, bg='#0089FF', fg='#FFFFFF', anchor=Tkinter.W).grid(ipadx=5, row=0, column=0, sticky=Tkinter.W)
Tkinter.Label(root, text="Line", bd=1, bg='#0089FF', fg='#FFFFFF', anchor=Tkinter.W).grid(ipadx=5, row=0, column=1)
Tkinter.Label(root, text="Destination", bd=1, bg='#0089FF', fg='#FFFFFF', anchor=Tkinter.W).grid(ipadx=5, row=0, column=2, sticky=Tkinter.W)
Tkinter.Label(root, text="Time", bd=1, bg='#0089FF', fg='#FFFFFF', anchor=Tkinter.W).grid(ipadx=5, row=0, column=3, sticky=Tkinter.E)
for traffic in traffics:
  if r % 2:
    bg = '#FFFFFF' 
  else:
    bg = '#CCCCCC'
  Tkinter.Label(root, text=traffic['TransportMode'], bd=1, bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=0, sticky=Tkinter.W)
  Tkinter.Label(root, text=traffic['LineNumber'], bd=1, bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=1)
  Tkinter.Label(root, text=traffic['Destination'], bd=1, bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=2, sticky=Tkinter.W)
  Tkinter.Label(root, text=traffic['DisplayTime'], bd=1, bg=bg, anchor=Tkinter.W).grid(ipadx=5, row=r, column=3, sticky=Tkinter.E)
  r=r+1

Tkinter.Label(root, text=sl_ins.time, bg='#0089FF', fg='#FFFFFF').grid(ipadx=5, row=r, columnspan=4, sticky=Tkinter.E)

root.mainloop()
