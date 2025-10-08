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
shaft.AddSection(0,15,30,15)
shaft.AddSection(30,17.5,44,17.5)
shaft.AddSection(44,21,90,21)
shaft.AddSection(90,25,190,25)
shaft.AddSection(190,21,245,21)
shaft.AddSection(245,17.5,255,17.5)
shaft.AddSection(255,15,286,15)
shaft.AddForce(70, 10, False, True, -876)
shaft.AddForce(70, 150, True, True, 2400)
shaft.AddForce(215, 10, False, True, -3937)
shaft.AddForce(215, 33.5, True, True, -10814)
shaft.ModifySupport(20,0)
shaft.ModifySupport(270,1)

print(shaft.forces_xz)

control = ShaftControl.ShaftController(shaft, main_win)

#teste
control.UpdateSectionTreeview()
control.UpdateForceTreeview()
control.UpdateCanvas()

main_win.SetController(control)
main_win.run()
