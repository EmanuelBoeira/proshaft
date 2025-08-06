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
control = ShaftControl.ShaftController(shaft, main_win)

main_win.SetController(control)
main_win.run()
