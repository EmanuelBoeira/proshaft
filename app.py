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
shaft.AddSection(0,10,250,10)
shaft.AddForce(50, 10, False, True, -876)
shaft.AddForce(50, 10, False, False, 2400)
shaft.AddForce(195, 10, False, True, -3937)
shaft.AddForce(195, 10, False, False, -10814)
shaft.AddSupport(0,0)
shaft.AddSupport(250,1)

control = ShaftControl.ShaftController(shaft, main_win)
control.UpdateSectionTreeview()
control.UpdateForceTreeview()
control.UpdateCanvas()

main_win.SetController(control)
main_win.run()
