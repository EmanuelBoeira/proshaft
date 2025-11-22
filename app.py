#arquivo principal
import sys
sys.path.append('./model/')
sys.path.append('./view/')
sys.path.append('./controller/')

import tkinter as tk

import ShaftModel as Shaft
import ShaftMainWin as MainWin
import ShaftController as ShaftControl


#start the aplication
main_win = MainWin.ShaftMainWindow()
shaft = Shaft.Shaft()

#teste
shaft.AddSection(30,30)
shaft.AddSection(35, 14)
shaft.AddSection(42, 46)
shaft.AddSection(50, 100)
shaft.AddSection(42, 55)
shaft.AddSection(35, 10)
shaft.AddSection(30,31)
shaft.AddForce(70, 0, True, -876)
shaft.AddForce(70, 150, False, 2400)
shaft.AddForce(215, 0, True, -3937)
shaft.AddForce(215, 33.5, False, -10814)
shaft.ModifySupport(20,0)
shaft.ModifySupport(270,1)

control = ShaftControl.ShaftController(shaft, main_win)

#teste
control.shaft_total_length = 286.0
control.UpdateSectionTreeview()
control.UpdateForceTreeview()
control.UpdateCanvas()

main_win.SetController(control)
main_win.run()
