#controller for shaft project
#remake this shit
#imports{{{
import sys
sys.path.append('../model/')
sys.path.append('../view/')

import tkinter as tk
import matplotlib.pyplot as plt
#import numpy as np

import ShaftModel as Shaft
import ShaftMainWin as MainWin
#}}}

#Class ShaftController{{{
class ShaftController:
	#init the class
	def __init__(self, model, view):
		self.model = model
		self.view = view

		#define quais botoẽs estarão disponíveis na inicialização
		#if (self.model.sections == []):
			#self.view.buttonDelSection.state(['disabled'])
			#self.view.buttonCalc.state(['disabled'])

	#add a section to the model shaft
	def AddSectionToModel(self, x1, y1, x2, y2):
		if self.model.sections == []:
			self.model.AddSection(x1, y1, x2, y2)
		else:
			x = float(self.model.sections[-1][1][0])
			self.model.AddSection(x, y1, (x+x2), y2)

	#remove section
	def RemoveSection(self, i):
		#for section in self.model.sections:
			#print(i)
			#if self.model.sections.index(section) >= i:
				#print(self.model.sections)
				#self.model.RemoveSection(self.model.sections.index(section))
		for x in range(len(self.model.sections)-i):
			self.model.RemoveSection(i)


	#add methods to add e remove stress
	def AddStressToModel(self, stress, x, l, b):
		self.model.AddStress(x, l, b, stress)

	def RemoveStress(self, i):
		for stress in self.model.stress:
			self.model.RemoveStress(i)

	#update the informations of sections treeview
	def UpdateSectionTreeview(self):
		#clean treeview
		for i in self.view.tree_sections.get_children():
			self.view.tree_sections.delete(i)
		#if has sections of the shaft, they are add to treeview		
		if self.model.sections != []:
			for section in self.model.sections:
				self.view.tree_sections.insert('', tk.END, text='D: %s mm L: %s mm'%(((section[0][1])*2, (section[1][0]-section[0][0]))))

		if self.model.stress != []:
			for stress in self.model.stress:
				self.view.tree_sections.insert('', tk.END, text='Chaveta x: %s mm'%(stress[0]))
				

	#add force to model
	def AddForceToModel(self, x, y, tangential, plane_xy, F):
		self.model.AddForce(x, y, tangential, plane_xy, F)

	#remove force
	def RemoveForce(self, i):
		self.model.RemoveForce(i)

	#modify the distance x of the support i
	def ModifySupport(self, x, i):
		self.model.AddSupport(x, i)

	#update the info of treeview forces
	def UpdateForceTreeview(self):
		#clean treeview
		for i in self.view.tree_forces.get_children():
			self.view.tree_forces.delete(i)
		#put the forces info in treeview
		if self.model.forces != []:
			for force in self.model.forces:
				self.view.tree_forces.insert('', tk.END, text='F: %s N'%(force[4]))

	#{{{update canvas_long and canvas_axial
	def UpdateCanvas(self):
		#clean canvas
		self.view.canvas_long.delete('all')
		self.view.canvas_axial.delete('all')

		self.view.DrawOrientationCanvas()

		if self.model.sections != []:
			fator = 1

			#identify the factor of scale to draw the sections inside the canvas
			if int(self.model.sections[-1][1][0]) > 400:
				fator = 400/self.model.sections[-1][1][0]

			for section in self.model.sections:
				if int((section[0][1]*2)) > 200:
					if (200/int(section[0][1]*2)) < fator:
						fator = 220/int(section[0][1]*2)

			#comprimento total em x ao somar todas as seções
			Ltotal = int(self.model.sections[-1][1][0]*fator)

			#draw the section os the shaft.
			for section in self.model.sections:
				self.view.canvas_long.create_rectangle((int((210-(Ltotal/2))+(section[0][0]*fator)), int((125-(section[0][1]*fator)))), (int((210-(Ltotal/2))+(section[1][0]*fator)), int((125+(section[1][1]*fator)))), outline='black', width=2)

				radius = 0

				if section[0][1] > radius:
					radius = section[0][1]
					self.view.canvas_axial.create_oval((int(125-radius*fator), int(125-radius*fator)),(int(125+radius*fator),int(125+radius*fator)), outline='black', width=2)

			#draw arrows for each force in the model
			for force in self.model.forces:
				if force[3]:
					drawArrowV(self.view.canvas_long, (210-(Ltotal/2))+(float(force[0])*fator), 125-(float(force[1]))*fator, True if force[4] > 0 else False)
				elif not force[3]:
					if force[2]:
						drawArrowH(self.view.canvas_axial, 125, 125-float(force[1])*fator, True if force[4] > 0 else False)
					elif not force[2]:
						drawArrowH(self.view.canvas_axial, 125+float(force[1])*fator, 125, True if force [4] > 0 else False)

			for support in self.model.supports:
				drawSupport(self.view.canvas_long, (210-(Ltotal/2))+float(support)*fator, 125+30)

			if self.model.stress != []:
				for stress in self.model.stress:
					if stress[3] == 'flat key':
						drawFlatKey(self.view.canvas_long, (210-(Ltotal/2))+stress[0]*fator , 125, stress[1]*fator, stress[2]*fator)
	#}}}

	def CalculateDminVonMisses(self):
		Shaft.Reactions(self.model)
		Shaft.Bending_Moment(self.model)
		x = []

		for f in self.model.forces:
			if x != []:
				if f[0] == x[-1]:
					continue
				else:
					x.append(f[0])
			else:
				x.append(f[0])
				self.model.mtot.insert(0, f[0])

		self.model.mtot.append(0)

		fig, ax = plt.subplots()
		ax.plot(x, self.model.mtot)
		plt.show()
#}}}

#Function drawArrowV{{{
#functions to draw elements in canvas
def drawArrowV(canvas, x, y, positive):
	if positive:
		canvas.create_polygon(((x+5,y+5),(x,y),(x-5,y+5)),fill='red')
		canvas.create_line(((x,y+5),(x,y+25)),width=4,fill='red')

	else:
		canvas.create_polygon(((x-5,y-5),(x,y),(x+5,y-5)),fill='red')
		canvas.create_line(((x,y-5),(x,y-25)),width=4,fill='red')
#}}}

#Function drawArrowH{{{
def drawArrowH(canvas, x, y, positive):
	if positive:
		canvas.create_polygon(((x,y),(x-5,y+5),(x-5,y-5)), fill='red')
		canvas.create_line(((x-5, y),(x-25,y)), width=4, fill='red')
	
	else:
		canvas.create_polygon(((x,y),(x+5,y-5),(x+5,y+5)), fill='red')
		canvas.create_line(((x+5, y),(x+25,y)), width=4, fill='red')
#}}}

#Function drawSupport{{{
def drawSupport(canvas, x, y):
	canvas.create_polygon(((x-10,y+10),(x,y),(x+10,y+10)), fill='black')
#}}}

#Function drawKey{{{
def drawFlatKey(canvas, x, y, l, b):
	canvas.create_rectangle(((x+(b/2),y-(b/2)),(x+l-(b/2), y+(b/2))), outline='black', width=2)
	canvas.create_oval(((x, y-(b/2)),(x+b, y+(b/2))), outline='black', width=2)
	canvas.create_oval(((x+l-b, y-(b/2)),(x+l, y+(b/2))), outline='black', width=2)
	canvas.create_rectangle(((x+(b/2),y-(b/2)+2),(x+l-(b/2), y+(b/2)-2)), outline='white', fill='white', width=2)
#}}}
