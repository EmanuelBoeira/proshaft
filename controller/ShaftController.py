#controller for shaft project
#remake this shit
#imports{{{
import sys
sys.path.append('../model/')
sys.path.append('../view/')

import tkinter as tk
from tkinter.messagebox import showwarning

import ShaftModel as Shaft
import ShaftProjectModel as ShaftProject
import ShaftMainWin as MainWin
#}}}

#Class ShaftController{{{
class ShaftController:
	
	shaft_project = ShaftProject.ShaftProject()
	shaft_total_length = 0

	#init{{{
	#init the class
	def __init__(self, model, view):
		self.model = model
		self.view = view

		#define quais botoẽs estarão disponíveis na inicialização
		if (self.model.sections == []):
			self.view.button_next.config(state=tk.DISABLED)
	#}}}
	#AddSectionToModel{{{
	#add a section to the model shaft
	def AddSectionToModel(self, diamiter, length):
		self.model.AddSection(diamiter, length)
		self.shaft_total_length = self.shaft_total_length + length
	#}}}
	#RemoveSection{{{
	#remove section
	def RemoveSection(self, i):
		for x in range(len(self.model.sections)-i):
			self.shaft_total_length = self.shaft_total_length - self.model.sections[i][1]
			self.model.RemoveSection(i)
	#}}}
	#AddStressToModel{{{
	def AddStressToModel(self, x_stress, stress, variables):
		x = 0

		if self.shaft_total_length > x_stress:
			for section in self.model.sections:
				if x_stress >= x and x_stress < x+section[1]:
					if stress == 'stop ring':
						if section[0] > variables[0]:
							self.model.AddStress(x_stress, section[0], stress, variables)
							break
						else:
							showwarning(title='Diâmetro inadequado', message='Valor de d ultrapassa o diâmetro desta seção do eixo.')
							break

					elif stress == 'flat key':
						self.model.AddStress(x_stress, section[0], stress, variables)
						break

				x = x + section[1]
		else:
			showwarning(title='Posição inadequada', message='Valor de x ultrapassa o comprimento total do eixo.')
	#}}}
	#RemoveStress{{{
	#remove stress from the model
	def RemoveStress(self, i):
		for stress in self.model.stress:
			self.model.RemoveStress(i)
	#}}}
	#UpdateSectionTreeview{{{
	#update the informations of sections treeview
	def UpdateSectionTreeview(self):
		#clean treeview
		for i in self.view.tree_sections.get_children():
			self.view.tree_sections.delete(i)
		#if has sections of the shaft, they are add to treeview		
		if self.model.sections != []:
			for section in self.model.sections:
				self.view.tree_sections.insert('', tk.END, text='D: %s mm L: %s mm'%(section[0], section[1]))
	#}}}
	#UpdateStressTreeview{{{
	#update the informations of stress treeview
	def UpdateStressTreeview(self):
		for i in self.view.tree_stress.get_children():
			self.view.tree_stress.delete(i)
		if self.model.stress != []:
			for stress in self.model.stress:
				self.view.tree_stress.insert('', tk.END, text='%s, x: %s mm'%(stress[2], stress[0]))
	#}}}
	#UpdateForceTreeview{{{
	#update the info of treeview forces
	def UpdateForceTreeview(self):
		#clean treeview
		for i in self.view.tree_forces.get_children():
			self.view.tree_forces.delete(i)
		#put the forces info in treeview
		if self.model.forces_xy != []:
			for force in self.model.forces_xy:
				self.view.tree_forces.insert('', tk.END, text='F(XY): %s mm, %s N'%(force[0], force[2]))
		if self.model.forces_xz != []:
			for force in self.model.forces_xz:
				self.view.tree_forces.insert('', tk.END, text='F(XZ): %s mm, %s N'%(force[0], force[2]))
	#}}}
	#AddForceToModel{{{
	#add force to model
	def AddForceToModel(self, x, y, plane_xy, F):
		if self.shaft_total_length > x:
			self.model.AddForce(x, y, plane_xy, F)
		else:
			showwarning(title='Posição inadequada', message='Valor de x ultrapassa o comprimento total do eixo.')
	#}}}
	#RemoveForce{{{
	#remove force from model
	def RemoveForce(self, i):
		if i >= len(self.model.forces_xy):
			self.model.RemoveForce(i-len(self.model.forces_xy), False)
		else:
			self.model.RemoveForce(i, True)
	#}}}
	#ModifySupport{{{
	#modify the distance x of the support i
	def ModifySupport(self, x, i):
		if self.shaft_total_length> x:
			self.model.ModifySupport(x, i)
		else:
			showwarning(title='Posição inadequada', message='Valor de x ultrapassa o comprimento total do eixo.')
	#}}}
	#UpdateCanvas{{{
	#update long canvas
	def UpdateCanvas(self):
		#clean canvas
		self.view.canvas_long.delete('all')

		self.view.DrawOrientationCanvas()

		if self.model.sections != []:
			#habilita botão next
			if self.view.button_next["state"] != "normal":
				self.view.button_next.config(state=tk.NORMAL)

			#identify the factor of scale to draw the sections inside the canvas{{{
			fator = 1

			for section in self.model.sections:
				if section[0] > fator:
					fator = section[0]

			if (220/fator) < (660/self.shaft_total_length):
				fator = 220/fator
			else:
				fator = 660/self.shaft_total_length

			#}}}
			
			#total length of shaft in x
			Ltotal = int(self.shaft_total_length*fator)
			#x position for draw sections
			x = 0

			#draw sections of shaft{{{
			for section in self.model.sections:
				self.view.canvas_long.create_rectangle((int(340-(Ltotal/2)+x), int(125-(section[0]*fator/2))), (int(340-(Ltotal/2)+x+(section[1]*fator)), int(125+(section[0]*fator/2))), outline='black', width=2)
				x = x + (section[1]*fator)
			#}}}
			#draw stress concentration{{{
			if self.model.stress != []:
				for stress in self.model.stress:
					if stress[2] == 'flat key':
						drawFlatKey(self.view.canvas_long, (340-(Ltotal/2))+stress[0]*fator , 125, stress[3][0]*fator, stress[3][1]*fator)
					elif stress[2] == 'stop ring':
						drawStopRing(self.view.canvas_long, (340-(Ltotal/2))+stress[0]*fator, 125, stress[1]*fator, stress[3][0]*fator, stress[3][1]*fator)
			#}}}
			#draw arrows for each force{{{
			#forces XY
			for force in self.model.forces_xy:
				drawForceY(self.view.canvas_long, (340-(Ltotal/2))+(float(force[0])*fator), 125, True if force[2] > 0 else False)
				if force[1] != 0:
					drawCircArrow(self.view.canvas_long, (340-(Ltotal/2))+(float(force[0])*fator), 125, True if (force[2] > 0 and force[1] < 0) or (force[2] < 0 and force[1] > 0) else False)
			#forces XZ
			for force in self.model.forces_xz:
				if force[2] <= 0:
					drawForceZ(self.view.canvas_long, (340-(Ltotal/2))+(float(force[0])*fator), 125)
				if force[1] != 0:
					drawCircArrow(self.view.canvas_long, (340-(Ltotal/2))+(float(force[0])*fator), 125, True if (force[2] > 0 and force[1] > 0) or (force[2] < 0 and force[1] < 0) else False)
			#}}}
			#draw supports{{{
			drawSupportPin(self.view.canvas_long, (340-(Ltotal/2))+float(self.model.supports[0])*fator, 125)
			drawSupportRoller(self.view.canvas_long, (340-(Ltotal/2))+float(self.model.supports[1])*fator, 125)
			#}}}
		else:
			self.view.button_next.config(state=tk.DISABLED)
	#}}}
	#CalculateShaft{{{
	def CalculateShaft(self, material, fabrication_method):
		if material == '':
			showwarning(title='Material não definido!', message='Defina um material para o eixo.')
		elif self.model.supports[0] == self.model.supports[1]:
			showwarning(title='Suportes sobrepostos!', message='Os suportes não podem estar a mesma posição! Por favor edite pelo menos um dos suportes.')
		else:
			self.shaft_project.Clean()
			self.shaft_project.DefineMaterial(material, fabrication_method)
			self.shaft_project.GeneratePlots(self.model)
			print(self.shaft_project.material)
			
	#}}}
	#clean the values calculated in project{{{
	def CleanCalc(self):
		self.shaft_project.Clean()
	#}}}
	#PlotInCanvas{{{
	#plot math data in canvas from the last frame
	def PlotInCanvas(self, plot):
		self.view.canvas_plots.delete('all')

		if plot == 'F(XY)':
			drawPlot(self.view.canvas_plots, self.shaft_project.plot_f_xy, 100, 250, 'F(kN)')

		if plot == 'F(XZ)':
			drawPlot(self.view.canvas_plots, self.shaft_project.plot_f_xz, 100, 250, 'F(kN)')

		if plot == 'F(TOT)':
			drawPlot(self.view.canvas_plots, self.shaft_project.plot_f_tot, 100, 250, 'F(kN)')

		if plot == 'M(XY)':
			drawPlot(self.view.canvas_plots, self.shaft_project.plot_m_xy, 100, 250, 'M(N.m)')

		if plot == 'M(XZ)':
			drawPlot(self.view.canvas_plots, self.shaft_project.plot_m_xz, 100, 250, 'M(N.m)')

		if plot == 'M(TOT)':
			drawPlot(self.view.canvas_plots, self.shaft_project.plot_m_tot, 100, 250, 'M(N.m)')

		if plot == 'Torque':
			drawPlot(self.view.canvas_plots, self.shaft_project.plot_t, 100, 250, 'T(N.m)')
	#}}}
	#CalculateGoodman{{{
	def CalculateGoodman(self):
		self.shaft_project.CalcGoodman()
	#}}}
	#CalculateASME{{{
	def CalculateASME(self):
		self.shaft_project.CalcASME(self.model)
	#}}}
#}}}

#drawForces{{{
def drawForceY(canvas, x, y, positive) -> None:
	if positive:
		canvas.create_polygon(((x+10,y+20),(x,y),(x-10,y+20)), outline='black', fill='green')
		canvas.create_rectangle((x-3, y+20),(x+3, y+80), fill='green', outline='black')
		canvas.create_line(((x-3,y+20),(x+3,y+20)), width=4, fill='green')

	else:
		canvas.create_polygon(((x-10,y-20),(x,y),(x+10,y-20)), outline='black', fill='green')
		canvas.create_rectangle((x-3, y-20),(x+3, y-80), fill='green', outline='black')
		canvas.create_line(((x-3,y-20),(x+3,y-20)),width=4, fill='green')

def drawForceZ(canvas, x, y) -> None:
	canvas.create_oval(((x-10, y-10),(x+10, y+10)), outline='black', fill='blue')
	canvas.create_oval(((x-3, y-3),(x+3, y+3)), outline='black', fill='blue')

def drawForceX(canvas, x, y, positive):
	if positive:
		canvas.create_polygon(((x,y),(x-20,y+10),(x-20,y-10)), fill='red')
		canvas.create_rectangle((x-20, y-3),(x-80, y+3), fill='red', outline='black')
		canvas.create_line(((x-20, y-3),(x-20,y+3)), width=4, fill='red')
	
	else:
		canvas.create_polygon(((x,y),(x+20,y-10),(x+20,y+10)), fill='red')
		canvas.create_rectangle((x+20, y-3),(x+80, y+3), fill='red', outline='black')
		canvas.create_line(((x+20, y-3),(x+20,y+3)), width=4, fill='red')
#}}}

#Function drawCircArrow{{{
def drawCircArrow(canvas, x, y, clockwise):
	if clockwise:
		canvas.create_arc((x-60, y+60), (x+60, y-60), start=330, extent=60, style=tk.ARC, width=6, outline='red')
		canvas.create_polygon((x+43, y-22.5), (x+61, y-36.5), (x+42, y-43.7), fill='red')
	else:
		canvas.create_arc((x-60, y+60), (x+60, y-60), start=150, extent=60, style=tk.ARC, width=6, outline='red')
		canvas.create_polygon((x-43, y-22.5), (x-61, y-36.5), (x-42, y-43.7), fill='red')
#}}}

#Function drawSupport{{{
def drawSupportPin(canvas, x, y):
	canvas.create_polygon(((x-10,y+10),(x,y),(x+10,y+10)), fill='black')
	canvas.create_line(((x-15, y+10),(x+15, y+10)), width=2, fill='black')
	canvas.create_line(((x-10, y+10),(x-15, y+15)), width=2, fill='black')
	canvas.create_line(((x, y+10),(x-5, y+15)), width=2, fill='black')
	canvas.create_line(((x+10, y+10),(x+5, y+15)), width=2, fill='black')

def drawSupportRoller(canvas, x, y):
	canvas.create_polygon(((x-10,y+10),(x,y),(x+10,y+10)), fill='black')
	canvas.create_line(((x-15, y+10),(x+15, y+10)), width=2, fill='black')
	canvas.create_line(((x-15, y+15),(x+15, y+15)), width=2, fill='black')
#}}}

#Function drawFlatKey{{{
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
def drawPlot(canvas, points, x, y, t):
	#540x290
	#print(points)

	p_max = 1
	p_min = 0

	for point in points:
		if p_max < point[1]:
			p_max = point[1]
		if p_min > point[1]:
			p_min = point[1]

	x_scale = 300/points[-1][0]
	y_scale = 200/(p_max - p_min)

	canvas.create_line((x, y+(p_min*y_scale)), (x+350, y+(p_min*y_scale)), width=2, fill='black')
	canvas.create_line((x, y), (x, y-205), width=2, fill='black')
	canvas.create_polygon((x+355,y+(p_min*y_scale)),(x+345, y+(p_min*y_scale)-8),(x+345, y+(p_min*y_scale)+8), fill='black')
	canvas.create_polygon((x,y-215),(x+8, y-205),(x-8, y-205), fill='black')
	canvas.create_text(x+380, y+5+(p_min*y_scale), text='x(mm)', fill='black')
	canvas.create_text(x, y-230, text=t, fill='black')


	for i in range(len(points)-1):
		#linhas do gráfico
		canvas.create_line((x+(points[i][0])*x_scale, y+(p_min*y_scale)-(points[i][1]*y_scale)),(x+(points[i+1][0]*x_scale), y+(p_min*y_scale)-(points[i+1][1]*y_scale)), width=3, fill='blue')

		#linhas de pontos
		canvas.create_line((x+ (points[i][0]*x_scale), y+(p_min*y_scale)+5), (x+(points[i][0]*x_scale), y+(p_min*y_scale)-5), width=3, fill='black')
		canvas.create_rectangle((x-10+(points[i][0]*x_scale), y+(p_min*y_scale)+5), (x+(points[i][0]*x_scale+10), y+(p_min*y_scale)+20), fill='white', outline='white')
		canvas.create_text((x+(points[i][0]*x_scale), y+(p_min*y_scale)+15),text=points[i][0], fill='black')

		if points[i+1][1] != points[i][1]:
			canvas.create_line((x+5, y+(p_min*y_scale)-(points[i][1]*y_scale)), (x-5, y+(p_min*y_scale)-(points[i][1]*y_scale)), width=2, fill='black')
			canvas.create_text((x-35, y+(p_min*y_scale)-(points[i][1]*y_scale)),text='{:.1f}'.format(points[i][1]/1000), fill='black')
#}}}
