#controller for shaft project
#remake this shit
#imports{{{
import sys
sys.path.append('../model/')
sys.path.append('../view/')

import tkinter as tk
from tkinter.messagebox import showwarning
#import matplotlib.pyplot as plt
#import numpy as np

import ShaftModel as Shaft
import ShaftMainWin as MainWin
#}}}

#Class ShaftController{{{
class ShaftController:
	#init
	#init the class{{{
	def __init__(self, model, view):
		self.model = model
		self.view = view

		#define quais botoẽs estarão disponíveis na inicialização
		#if (self.model.sections == []):
			#self.view.buttonDelSection.state(['disabled'])
			#self.view.buttonCalc.state(['disabled'])
	#}}}

	#add a section to the model shaft
	#AddSectionToModel{{{
	def AddSectionToModel(self, x1, y1, x2, y2):
		if self.model.sections == []:
			self.model.AddSection(x1, y1, x2, y2)
		else:
			x = float(self.model.sections[-1][1][0])
			self.model.AddSection(x, y1, (x+x2), y2)
	#}}}

	#remove section
	#RemoveSection{{{
	def RemoveSection(self, i):
		for x in range(len(self.model.sections)-i):
			self.model.RemoveSection(i)
	#}}}

	#add methods to add e remove stress
	#AddStressToModel{{{
	def AddStressToModel(self, stress, variables):
		if stress == 'stop ring':
			for section in self.model.sections:
				if section[1][0] >= variables[0]:
					variables.append(section[0][1]*2)
				else:
					variables.append(0)
		self.model.AddStress(stress, variables)
	#}}}

	#remove stress from the model
	#RemoveStress{{{
	def RemoveStress(self, i):
		for stress in self.model.stress:
			self.model.RemoveStress(i)
	#}}}

	#update the informations of sections treeview
	#UpdateSectionTreeview{{{
	def UpdateSectionTreeview(self):
		#clean treeview
		for i in self.view.tree_sections.get_children():
			self.view.tree_sections.delete(i)
		#if has sections of the shaft, they are add to treeview		
		if self.model.sections != []:
			for section in self.model.sections:
				self.view.tree_sections.insert('', tk.END, text='D: %s mm L: %s mm'%(((section[0][1])*2, (section[1][0]-section[0][0]))))
	#}}}

	#update the informations of stress treeview
	#UpdateStressTreeview{{{
	def UpdateStressTreeview(self):
		for i in self.view.tree_stress.get_children():
			self.view.tree_stress.delete(i)
		if self.model.stress != []:
			for stress in self.model.stress:
				self.view.tree_stress.insert('', tk.END, text='%s, x: %s mm'%(stress[0], stress[1][0]))
	#}}}

	#update the info of treeview forces
	#UpdateForceTreeview{{{
	def UpdateForceTreeview(self):
		#clean treeview
		for i in self.view.tree_forces.get_children():
			self.view.tree_forces.delete(i)
		#put the forces info in treeview
		if self.model.forces_xy != [] and self.model.forces_xz != []:
			for force in self.model.forces_xy:
				self.view.tree_forces.insert('', tk.END, text='F(XY): %s N'%(force[2]))
			for force in self.model.forces_xz:
				self.view.tree_forces.insert('', tk.END, text='F(XZ): %s N'%(force[2]))
	#}}}

	#add force to model
	#AddForceToModel{{{
	def AddForceToModel(self, x, y, tangential, plane_xy, F):
		if self.model.sections[-1][1][0] > x:
			self.model.AddForce(x, y, tangential, plane_xy, F)
		else:
			showwarning(title='Posição inadequada', message='Valor de x ultrapassa o comprimento total do eixo.')
	#}}}

	#remove force from model
	#RemoveForce{{{
	def RemoveForce(self, i):
		if i >= len(self.model.forces_xy):
			self.model.RemoveForce(i-len(self.model.forces_xy), False)
		else:
			self.model.RemoveForce(i, True)
	#}}}

	#modify the distance x of the support i
	#ModeifySupport{{{
	def ModifySupport(self, x, i):
		if self.model.sections[-1][1][0] > x:
			self.model.AddSupport(x, i)
		else:
			showwarning(title='Posição inadequada', message='Valor de x ultrapassa o comprimento total do eixo.')
	#}}}

	#update long and axal canvas
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

			for f in self.model.forces_xy:
				if int(f[1]*2) > 200:
					if int(200/(f[1]*2)) < fator:
						fator = 200/(f[1]*2)

			for f in self.model.forces_xz:
				if int(f[1]*2) > 200:
					if int(200/(f[1]*2)) < fator:
						fator = 200/(f[1]*2)

			#total length of shaft in x
			Ltotal = int(self.model.sections[-1][1][0]*fator)

			#draw the section os the shaft.
			for section in self.model.sections:
				self.view.canvas_long.create_rectangle((int((210-(Ltotal/2))+(section[0][0]*fator)), int((125-(section[0][1]*fator)))), (int((210-(Ltotal/2))+(section[1][0]*fator)), int((125+(section[1][1]*fator)))), outline='black', width=2)

				radius = 0
				
				if section[0][1] > radius:
					radius = section[0][1]
					self.view.canvas_axial.create_oval((int(125-radius*fator), int(125-radius*fator)),(int(125+radius*fator),int(125+radius*fator)), outline='black', width=2)

			#draws each type of stress concentration on canvas
			if self.model.stress != []:
				for stress in self.model.stress:
					if stress[0] == 'flat key':
						drawFlatKey(self.view.canvas_long, (210-(Ltotal/2))+stress[1][0]*fator , 125, stress[1][1]*fator, stress[1][2]*fator)
					if stress[0] == 'stop ring':
						drawStopRing(self.view.canvas_long, (210-(Ltotal/2))+stress[1][0]*fator, 125, stress[1][3]*fator, stress[1][1]*fator, stress[1][2]*fator)

			#draw arrows for each force in the model
			for force in self.model.forces_xy:
				if force[1] != 0:
					drawArrowH(self.view.canvas_axial, 125, 125-float(force[1])*fator, True if force[2] > 0 else False)
				elif force[1] == 0:
					drawArrowV(self.view.canvas_long, (210-(Ltotal/2))+(float(force[0])*fator), 125-(float(force[1]))*fator, True if force[2] > 0 else False)

			for force in self.model.forces_xz:
				if force[1] != 0:
					drawArrowH(self.view.canvas_axial, 125, 125-float(force[1])*fator, True if force[2] > 0 else False)
				elif force[1] == 0:
					drawArrowV(self.view.canvas_long, (210-(Ltotal/2))+(float(force[0])*fator), 125-(float(force[1]))*fator, True if force[2] > 0 else False)

			for support in self.model.supports:
				drawSupport(self.view.canvas_long, (210-(Ltotal/2))+float(support)*fator, 125+30)
	#}}}

	#calculate reactions em bending moments
	#CalculateShaft{{{
	def CalculateShaft(self):
		Shaft.Reactions(self.model)
		Shaft.Bending_Moment(self.model)
		#x = []
		#mom = []
		#for f in self.model.forces:
		#	if x != []:
		#		if f[0] == x[-1]:
		#			continue
		#		else:
		#			x.append(f[0])
		#	else:
		#		x.append(f[0])
		#		self.model.mtot.insert(0, f[0])

		#self.model.mtot.append(0)

		#self.model.moments_xy.insert(0, [0,0])

		#drawPlot(self.view.canvas_plots, self.model.moments_xy, 200, 200)

		#for m in self.model.moments_xy:
		#	x.append(m[0])
		#	mom.append(m[1])

		#fig, ax = plt.subplots()
		#ax.plot(x, mom)
		#plt.show()
	#}}}

	#plot math data in canvas from the last frame
	#PlotInCanvas{{{
	def PlotInCanvas(self, plot):
		self.view.canvas_plots.delete('all')

		if plot == 'F(XY)':
			points = [[0,0]]
			points_to_add = []

			for force in self.model.forces_xy:
				points.append([force[0], force[2]])

			for i in range(len(points)-1):
				points[i+1][1] = points[i+1][1] + points[i][1]

			for i in range(len(points)-1):
				if points[i][0] != points[i+1][0]:
					points_to_add.append([i+1, [points[i+1][0], points[i][1]]])

			points_to_add.sort(reverse=True)

			for p in points_to_add:
				points.insert(p[0], p[1])

			drawPlot(self.view.canvas_plots, points, 100, 250)

		if plot == 'F(XZ)':
			points = [[0,0]]
			points_to_add = []

			for force in self.model.forces_xz:
				points.append([force[0], force[2]])

			for i in range(len(points)-1):
				points[i+1][1] = points[i+1][1] + points[i][1]

			for i in range(len(points)-1):
				if points[i][0] != points[i+1][0]:
					points_to_add.append([i+1, [points[i+1][0], points[i][1]]])

			points_to_add.sort(reverse=True)

			for p in points_to_add:
				points.insert(p[0], p[1])

			drawPlot(self.view.canvas_plots, points, 100, 250)

		if plot == 'F(TOT)':
			print('ftot')

		if plot == 'M(XY)':
			if self.model.moments_xy[0][1] != 0:
				self.model.moments_xy.insert(0, [0,0])
			drawPlot(self.view.canvas_plots, self.model.moments_xy, 100, 250)

		if plot == 'M(XZ)':
			if self.model.moments_xz[0][1] != 0:
				self.model.moments_xz.insert(0, [0,0])
			drawPlot(self.view.canvas_plots, self.model.moments_xz, 100, 250)

		if plot == 'M(TOT)':
			print('mtot...')

		if plot == 'Torque':
			points = [[0,0]]
			points_to_add = []

			for f in self.model.forces_xy:
				if f[1] != 0:
					points.append([f[0], f[1]*f[2]])

			for f in self.model.forces_xz:
				if f[1] != 0:
					points.append([f[0], f[1]*f[2]])

			points.sort()

			for i in range(len(points)-1):
				points[i+1][1] = points[i+1][1] + points[i][1]

			for i in range(len(points)-1):
				if points[i][0] != points[i+1][0]:
					points_to_add.append([i+1, [points[i+1][0], points[i][1]]])

			points_to_add.sort(reverse=True)

			for p in points_to_add:
				points.insert(p[0], p[1])

			drawPlot(self.view.canvas_plots, points, 100, 250)
	#}}}
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

#Function drawStopRing{{{
def drawStopRing(canvas, x, y, D, d, s):
	canvas.create_rectangle((x, y-(D/2)),(x+s, y+(D/2)), outline='white', fill='white', width=2)
	canvas.create_rectangle((x, y-(d/2)),(x+s, y+(d/2)), outline='black', fill='white', width=2)
	canvas.create_line((x, y-(D/2)),(x, y+(D/2)), fill='black', width=2)
	canvas.create_line((x+s, y-(D/2)),(x+s, y+(D/2)), fill='black', width=2)
#}}}

#Function drawPlot{{{
def drawPlot(canvas, points, x, y):
	#540x290
	print(points)

	p_max = 1
	p_min = 0

	for point in points:
		if p_max < point[1]:
			p_max = point[1]
		if p_min > point[1]:
			p_min = point[1]

	x_scale = 300/points[-1][0]
	y_scale = 200/(p_max - p_min)

	canvas.create_line((x, y+(p_min*y_scale)), (x+350, y+(p_min*y_scale)), width=3, fill='black')
	canvas.create_line((x, y), (x, y-205), width=3, fill='black')
	canvas.create_polygon((x+355,y+(p_min*y_scale)),(x+345, y+(p_min*y_scale)-8),(x+345, y+(p_min*y_scale)+8), fill='black')
	canvas.create_polygon((x,y-215),(x+8, y-205),(x-8, y-205), fill='black')

	for i in range(len(points)-1):
		#linhas do gráfico
		canvas.create_line((x+(points[i][0])*x_scale, y+(p_min*y_scale)-(points[i][1]*y_scale)),(x+(points[i+1][0]*x_scale), y+(p_min*y_scale)-(points[i+1][1]*y_scale)), width=3, fill='blue')

		#linhas de pontos
		canvas.create_line((x+ (points[i][0]*x_scale), y+(p_min*y_scale)+5), (x+(points[i][0]*x_scale), y+(p_min*y_scale)-5), width=3, fill='black')
		canvas.create_text((x+(points[i][0]*x_scale), y+(p_min*y_scale)+10),text=points[i][0], fill='black')

		if points[i+1][1] != points[i][1]:
			canvas.create_line((x+5, y+(p_min*y_scale)-(points[i][1]*y_scale)), (x-5, y+(p_min*y_scale)-(points[i][1]*y_scale)), width=3, fill='black')
			canvas.create_text((x-35, y+(p_min*y_scale)-(points[i][1]*y_scale)),text='{:.1f}'.format(points[i][1]/1000), fill='black')
		


#}}}
