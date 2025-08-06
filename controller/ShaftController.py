#controller for shaft project

import sys
sys.path.append('../model/')
sys.path.append('../view/')

import tkinter as tk

import ShaftModel as Shaft
import ShaftMainWin as MainWin

class ShaftController:
	#init the class
	def __init__(self, model, view):
		self.model = model
		self.view = view

		#define quais botoẽs estarão disponíveis na inicialização
		#if (self.model.sections == []):
			#self.view.buttonDelSection.state(['disabled'])
			#self.view.buttonOpenWinCarac.state(['disabled'])
			#self.view.buttonOpenWinSupport.state(['disabled'])
			#self.view.buttonOpenWinForce.state(['disabled'])
			#self.view.buttonDelForce.state(['disabled'])
			#self.view.buttonCalc.state(['disabled'])

	#add a section to the model shaft
	def AddSectionToModel(self, x1, y1, x2, y2):
		if self.model.sections == []:
			self.model.AddSection(x1, y1, x2, y2)
		else:
			x = 0
			for section in self.model.sections:
				x = section[1][0]

			self.model.AddSection(x, y1, (x+x2), y2)

	#update the informations of sections treeview
	def UpdateSectionTreeview(self):
		#clean treeview
		for i in self.view.tree_sections.get_children():
			self.view.tree_sections.delete(i)
		#if has sections of the shaft, they are add to treeview		
		if self.model.sections != []:
			for section in self.model.sections:
				self.view.tree_sections.insert('', tk.END, text='D: %s mm L: %s mm'%(((section[0][1])*2, (section[1][0]-section[0][0]))))

	#remove section
	def RemoveSection(self, i):
		self.model.RemoveSection(i)

	#add force to model
	def AddForceToModel(self, x, y, rt, plano, F):
		self.model.AddForce(x, y, rt, plano, F)

	#update the info of treeview forces
	def UpdateForceTreeview(self):
		#clean treeview
		for i in self.view.tree_forces.get_children():
			self.view.tree_forces.delete(i)
		#put the forces info in treeview
		if self.model.forces != []:
			for force in self.model.forces:
				self.view.tree_forces.insert('', tk.END, text='F: %s N'%(force[3]))

	#remove force
	def RemoveForce(self, i):
		self.model.RemoveForce(i)

	def AddSupportToModel(self, x, i):
		self.model.AddSupport(x, i)
		print(self.model.supports)

	#update canva_long and canva_axial
	def UpdateCanvas(self):
		if self.model.sections != []:
			#clean canvas
			self.view.canvas_long.delete('all')
			self.view.canvas_axial.delete('all')
			fator = 1

			#identify the factor of scale to draw the sections
			if int(self.model.sections[-1][1][0]) > 400:
				fator = 400/self.model.sections[-1][1][0]
			for section in self.model.sections:
				if int((section[0][1]*2)) > 200:
					if (200/int(section[0][1]*2)) < fator:
						fator = 220/int(section[0][1]*2)
			#comprimento total em x ao somar todas as seções
			Ltotal = int(self.model.sections[-1][1][0]*fator)

			#desenha as seções de eixo
			for section in self.model.sections:
				self.view.canvas_long.create_rectangle((int((210-(Ltotal/2))+(section[0][0]*fator)), int((125-(section[0][1]*fator)))), (int((210-(Ltotal/2))+(section[1][0]*fator)), int((125+(section[1][1]*fator)))), outline='black', width=2)
				radius = 0
				if section[0][1] > radius:
					radius = section[0][1]
					self.view.canvas_axial.create_oval((int(125-radius*fator), int(125-radius*fator)),(int(125+radius*fator),int(125+radius*fator)), outline='black', width=2)

#teste
#main_win = s_win.FirstWindow()
#shaft = Shaft.Shaft()
#control = ShaftController(shaft, main_win)

#main_win.SetController(control)
#main_win.run()

#print(shaft.sections)
#print(shaft.forces)
