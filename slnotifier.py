#!/usr/bin/python
import sl
import Tkinter
root = Tkinter.Tk()

sl_ins = sl.SL("9205", "2")
sl_ins.get_results()
traffics = sl_ins.traffics
r=0
for traffic in traffics:
  Tkinter.Label(root, text=traffic['TransportMode'], borderwidth=1).grid(row=r, column=0)
  Tkinter.Label(root, text=traffic['LineNumber'], borderwidth=1).grid(row=r, column=1)
  Tkinter.Label(root, text=traffic['Destination'], borderwidth=1).grid(row=r, column=2)
  Tkinter.Label(root, text=traffic['DisplayTime'], borderwidth=1).grid(row=r, column=3)
  r=r+1
root.mainloop()
