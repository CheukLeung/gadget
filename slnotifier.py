#!/usr/bin/python
import sl
import Tkinter
root = Tkinter.Tk()

sl_ins = sl.SL("9000", "1")
lines = sl_ins.get_results().splitlines()
r=0
for line in lines:
  Tkinter.Label(root, text=line, borderwidth=1).grid(row=r,column=0)
  r=r+1
root.mainloop()
