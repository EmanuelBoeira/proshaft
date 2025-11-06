from fpdf import FPDF
import webbrowser

#class for Shaft Project{{{
class ShaftProject:
	plot_f_xy  =    [] # [x, F]
	plot_f_xz  =    [] # [x, F]
	plot_f_tot =    [] # [x, Ftot]
	plot_m_xy  =    [] # [x, M]
	plot_m_xz  =    [] # [x, M]
	plot_m_tot =    [] # [x, Mtot]
	plot_t     =    [] # [x, T]
	material   =    [] # [material, Sut, Sy, Surface Factor]
	stress_points = [] # [x, d, Kf, Kfs]

	#init{{{
	def __init__(self, shaft, mat, fac):
		#clean the variables and aply initial conditions{{{
		self.plot_f_xy.append([0,0])
		self.plot_f_xz.append([0,0])
		self.plot_m_xy.append([0,0])
		self.plot_m_xz.append([0,0])
		self.plot_t.append([0,0])

		self.material.clear()
		if mat == "Aço 1050(temperado 800°F)":
			self.material.append(mat)
			self.material.append(1090)
			self.material.append(793)
			self.material.append(fac)
		elif mat == "Aço 1020(laminado a quente)":
			self.material.append(mat)
			self.material.append(379)
			self.material.append(207)
			self.material.append(fac)
		elif mat == "Aço 1040(laminado a quente)":
			self.material.append(mat)
			self.material.append(524)
			self.material.append(290)
			self.material.append(fac)
		elif mat == "Aço 1050(laminado a quente)":
			self.material.append(mat)
			self.material.append(621)
			self.material.append(345)
			self.material.append(fac)
		elif mat == "Alíminio":
			self.material.append(mat)
			self.material.append(55)
			self.material.append(15)
			self.material.append(fac)
		#}}}
		#add forces and torque from the shaft{{{
		for f in shaft.forces_xy:
			self.plot_f_xy.append([f[0], f[2]])

			if f[1] != 0:
				self.plot_t.append([f[0], f[1]*f[2]])

		for f in shaft.forces_xz:
			self.plot_f_xz.append([f[0], f[2]])

			if f[1] != 0:
				self.plot_t.append([f[0], f[1]*f[2]])

		#calculate the reactions on supports of shaft
		rxy1 = 0
		rxz1 = 0
		rxy2 = 0
		rxz2 = 0

		#calculate the reactions of the second support.
		for force in shaft.forces_xy:
			rxy2 = rxy2 + ((force[0]-shaft.supports[0]) * force[2])
		rxy2 = (-1)*rxy2/(shaft.supports[1]-shaft.supports[0])
		self.plot_f_xy.append([shaft.supports[1], rxy2])

		for force in shaft.forces_xz:
			rxz2 = rxz2 + ((force[0]-shaft.supports[0]) * force[2])
		rxz2 = (-1)*rxz2/(shaft.supports[1]-shaft.supports[0])
		self.plot_f_xz.append([shaft.supports[1], rxz2])

		#calculate the reactions of the first support.
		for force in self.plot_f_xy:
			rxy1 = rxy1 + force[1]
	
		for force in self.plot_f_xz:
			rxz1 = rxz1 + force[1]

		self.plot_f_xy.append([shaft.supports[0], (-1)*rxy1])
		self.plot_f_xz.append([shaft.supports[0], (-1)*rxz1])

		#sort the forces in order of x.
		self.plot_f_xy.sort()
		self.plot_f_xz.sort()
		#}}}
		#organize forces for plot{{{
		points_to_add = []

		#organize forces xy to plot
		for i in range(len(self.plot_f_xy)-1):
			self.plot_f_xy[i+1][1] = self.plot_f_xy[i+1][1] + self.plot_f_xy[i][1]

		for i in range(len(self.plot_f_xy)-1):
			if self.plot_f_xy[i][0] != self.plot_f_xy[i+1][0]:
				points_to_add.append([i+1, [self.plot_f_xy[i+1][0], self.plot_f_xy[i][1]]])

		points_to_add.sort(reverse=True)

		for p in points_to_add:
			self.plot_f_xy.insert(p[0], p[1])

		points_to_add = []

		#organize forces xz to plot
		for i in range(len(self.plot_f_xz)-1):
			self.plot_f_xz[i+1][1] = self.plot_f_xz[i+1][1] + self.plot_f_xz[i][1]

		for i in range(len(self.plot_f_xz)-1):
			if self.plot_f_xz[i][0] != self.plot_f_xz[i+1][0]:
				points_to_add.append([i+1, [self.plot_f_xz[i+1][0], self.plot_f_xz[i][1]]])

		points_to_add.sort(reverse=True)

		for p in points_to_add:
			self.plot_f_xz.insert(p[0], p[1])

		points_to_add = []

		#organize torques to plot
		for i in range(len(self.plot_t)-1):
			self.plot_t[i+1][1] = self.plot_t[i+1][1] + self.plot_t[i][1]

		for i in range(len(self.plot_t)-1):
			if self.plot_t[i][0] != self.plot_t[i+1][0]:
				points_to_add.append([i+1, [self.plot_t[i+1][0], self.plot_t[i][1]]])

		points_to_add.sort(reverse=True)

		for p in points_to_add:
			self.plot_t.insert(p[0], p[1])

		points_to_add = []
		#}}}
		#calculate bending mement by area{{{
		for i in range(len(self.plot_f_xy)-1):
			if self.plot_f_xy[i+1][0] != self.plot_f_xy[i][0]:
				self.plot_m_xy.append([self.plot_f_xy[i+1][0], self.plot_f_xy[i+1][1]*(self.plot_f_xy[i+1][0]-self.plot_f_xy[i][0])])

		for i in range(len(self.plot_m_xy)-1):
			self.plot_m_xy[i+1][1] = self.plot_m_xy[i][1] + self.plot_m_xy[i+1][1]

		for i in range(len(self.plot_f_xz)-1):
			if self.plot_f_xz[i+1][0] != self.plot_f_xz[i][0]:
				self.plot_m_xz.append([self.plot_f_xz[i+1][0], self.plot_f_xz[i+1][1]*(self.plot_f_xz[i+1][0]-self.plot_f_xz[i][0])])

		for i in range(len(self.plot_m_xz)-1):
			self.plot_m_xz[i+1][1] = self.plot_m_xz[i][1] + self.plot_m_xz[i+1][1]
		#}}}
		#Calculate Ftot{{{
		for f in self.plot_f_xy:
			if [f[0],0,0] not in self.plot_f_tot:
				self.plot_f_tot.append([f[0],0,0])

		for f in self.plot_f_xz:
			if [f[0],0,0] not in self.plot_f_tot:
				self.plot_f_tot.append([f[0],0,0])

		self.plot_f_tot.sort()

		for i in range(len(self.plot_f_tot)):
			if self.plot_f_xy != []:
				for j in range(len(self.plot_f_xy)-1):
					if self.plot_f_tot[i][0] >= self.plot_f_xy[j][0] and self.plot_f_tot[i][0] <= self.plot_f_xy[j+1][0]:
						self.plot_f_tot[i][1] = (self.plot_f_xy[j+1][1])**2
						#break

			if self.plot_f_xz != []:
				for j in range(len(self.plot_f_xz)-1):
					if self.plot_f_tot[i][0] >= self.plot_f_xz[j][0] and self.plot_f_tot[i][0] <= self.plot_f_xz[j+1][0]:
						self.plot_f_tot[i][2] = (self.plot_f_xz[j+1][1])**2
						#break

		for point in self.plot_f_tot:
			point[1] = (point[1] + point[2])**0.5
			point.pop(-1)

		for i in range(len(self.plot_f_tot)-1):
			if self.plot_f_tot[i][0] != self.plot_f_tot[i+1][0]:
				points_to_add.append([i+1, [self.plot_f_tot[i+1][0], self.plot_f_tot[i][1]]])

		points_to_add.sort(reverse=True)

		for p in points_to_add:
			self.plot_f_tot.insert(p[0], p[1])

		points_to_add = []
		#}}}
		#calculate Mtot{{{
		for m in self.plot_m_xy:
			self.plot_m_tot.append([m[0],0,0])

		for m in self.plot_m_xz:
			if [f[0]] not in self.plot_m_tot:
				self.plot_m_tot.append([m[0],0,0])

		self.plot_m_tot.sort()

		for i in range(len(self.plot_m_tot)):
			if self.plot_m_xy != []:
				for j in range(len(self.plot_m_xy)-1):
					if self.plot_m_tot[i][0] >= self.plot_m_xy[j][0] and self.plot_m_tot[i][0] <= self.plot_m_xy[j+1][0]:
						self.plot_m_tot[i][1] = (Get_y(self.plot_m_xy[j][0], self.plot_m_xy[j][1], self.plot_m_xy[j+1][0], self.plot_m_xy[j+1][1], self.plot_m_tot[i][0]))**2
						break

			if self.plot_m_xz != []:
				for j in range(len(self.plot_m_xz)-1):
					if self.plot_m_tot[i][0] >= self.plot_m_xz[j][0] and self.plot_m_tot[i][0] <= self.plot_m_xz[j+1][0]:
						self.plot_m_tot[i][2] = (Get_y(self.plot_m_xz[j][0], self.plot_m_xz[j][1], self.plot_m_xz[j+1][0], self.plot_m_xz[j+1][1], self.plot_m_tot[i][0]))**2
						break

		for point in self.plot_m_tot:
			point[1] = (point[1] + point[2])**0.5
			point.pop(-1)
		#}}}
		#adicionar pontos de interesse em stress_points{{{
		for s in shaft.stress:
			self.stress_points.append([s[0]+(s[3][0]/2), s[1], Kf(s[2], q_bending(s[1]/2, self.material[1])), Kfs(s[2], q_torsion(s[1]/2, self.material[1]))])

		for i in range(len(shaft.sections)-1):
			if shaft.sections[i][1][1] < shaft.sections[i+1][0][1]:
				self.stress_points.append([shaft.sections[i][1][0], shaft.sections[i][1][1]*2, Kf('diameter-0.02', q_bending(self.material[1])), Kfs('diameter-0.02', q_torsion(self.material[1]))])
			else:
				self.stress_points.append([shaft.sections[i+1][0][0], shaft.sections[i][0][1]*2, Kf('diameter-0.02', q_bending(self.material[1])), Kfs('diameter-0.02', q_torsion(self.material[1]))])

		self.stress_points.sort()
		print(self.stress_points)
		#}}}
	#}}}
	#clean{{{
	#This method clean the variables to recalculate without keep values
	def Clean(self):
		self.plot_f_xy.clear()
		self.plot_f_xz.clear()
		self.plot_f_tot.clear()
		self.plot_m_xy.clear()
		self.plot_m_xz.clear()
		self.plot_m_tot.clear()
		self.plot_t.clear()
		self.material.clear()
	#}}}
	#CalcGoodman{{{
	def CalcGoodman(self):
	
		Ma = 0
		Tm = 0

		for point in self.stress_points:
			for i in range(len(self.plot_m_tot)-1):
				if point[0] >= self.plot_m_tot[i][0] and point[0] < self.plot_m_tot[i+1][0]:
					Ma = Get_y(self.plot_m_tot[i][0], self.plot_m_tot[i][1], self.plot_m_tot[i+1][0], self.plot_m_tot[i+1][1], point[0])
					#break
			
			for i in range(len(self.plot_t)-1):
				if point[0] >= self.plot_t[i][0] and point[0] < self.plot_t[i+1][0]:
					Tm = self.plot_t[i][1]
					#break

		for point in self.stress_points:
			print(Goodman(point[1], Se(self.material[1], ka(self.material[1], self.material[3]), kb(point[1]), 1, 1, 1, 1), self.material[1], point[2], point[3], Ma, Tm))
	#}}}
	#CalcASME{{{
	def CalcASME(self, shaft):
	
		results = FPDF()
		results.add_page()
		results.set_font("Arial", size=12)
		results.set_fill_color(r=255, g=155, b=155)
		results.cell(180, 50, ln=2)

		Ma = 0
		Tm = 0

		for point in self.stress_points:
			for i in range(len(self.plot_m_tot)-1):
				if point[0] >= self.plot_m_tot[i][0] and point[0] < self.plot_m_tot[i+1][0]:
					Ma = Get_y(self.plot_m_tot[i][0], self.plot_m_tot[i][1], self.plot_m_tot[i+1][0], self.plot_m_tot[i+1][1], point[0])
					#break
			
			for i in range(len(self.plot_t)-1):
				if point[0] >= self.plot_t[i][0] and point[0] < self.plot_t[i+1][0]:
					Tm = self.plot_t[i][1]
					#break
			
			if Ma != 0:
				nf = ASME_Elliptic(point[1], Se(self.material[1], ka(self.material[1], self.material[3]), kb(point[1]), 1, 1, 0.814, 1), self.material[2], point[2], point[3], Ma, Tm)
			else:
				nf = 0

			results.cell(0,15, 'nf({}) = {}'.format(chr(97+self.stress_points.index(point)), nf), ln=2)

		drawShaftinPDF(results, shaft, self.stress_points)
		results.output("eixo.pdf")

		webbrowser.open('eixo.pdf')
	#}}}
#}}}

#Funcition DefineMaterial{{{
def DefineMaterial(material):

	materials_list = [[],[],[]] 

#}}}

#Function Se{{{
#function to calculate fatigue endurance limit.
def Se(Sut, ka=1, kb=1, kc=1, kd=1, ke=1, kf=1):
	return (0.5*Sut)*ka*kb*kc*kd*ke*kf
#}}}

#Function ka{{{
#function to calculate factor  ka.
def ka(Sut, factory='Usinado'):

	x = 0
	y = 0

	factory_methods = [['Retificado', 1.58, -0.085], ['Usinado', 4.51, -0.265], ['Laminado a quente', 57.7, -0.718], ['Forjado', 272, -0.995]]

	for factory_meyhod in factory_methods:
		if factory_meyhod[0] == factory:
			x = factory_meyhod[1]
			y = factory_meyhod[2]
			break

	return x*(Sut**y)
#}}}

#Function kb{{{
#function to calculate factor kb for torcion and bending.
def kb(d):
	if d <= 51 and d >= 2.8:
		return 1.24*(d**(-0.107))
	elif d > 51 and d <= 254:
		return 1.51 * (d*(-0.157))
	else:
		return 0
#}}}

#Function kd{{{
def kd(temp):
	temp = (temp*1.8)+32

	return 0.975+(0.000432*temp)-(0.00000115*(temp**2))+(0.00000000104*(temp**3))-(0.000000000000595*(temp**4))
#}}}

#Function ke{{{
def ke(conf):
	if conf == 50.0:
		return 1.0
	elif conf == 90.0:
		return 0.897
	elif conf == 95.0:
		return 0.868
	elif conf == 99.0:
		return 0.814
	elif conf == 99.9:
		return 0.753
#}}}

#Function Kf{{{
def Kf(stress, q):
	#list of stresses. [stress, Kt, Kts, value for selection]
	stress_list = [['diameter-0.02', 2.7, 2.2, 0.02], ['diameter-0.1', 1.7, 1.5, 0.1], ['flat key', 2.14, 3, 0.02], ['stop ring', 5, 3, 0]]

	for s in stress_list:
		if s[0] == stress:
			return 1+(q*(s[1]-1))
			break
#}}}

#Function Kfs{{{
def Kfs(stress, q):
	#list of stresses. [stress, Kt, Kts, value for selection]
	stress_list = [['diameter-0.02', 2.7, 2.2, 0.02], ['diameter-0.1', 1.7, 1.5, 0.1], ['flat key', 2.14, 3, 0.02], ['stop ring', 5, 3, 0]]

	for s in stress_list:
		if s[0] == stress:
			return 1+(q*(s[2]-1))
			break
#}}}

#Functions q{{{
#r é o raio do entalhe (entre 0 e 4 mm). Sut deve estar em MPa que é convertido em kpsi
def q_torsion(Sut, r=0.1):
	Sut = Sut*0.145
	return 1/(1+((0.19-(0.00251*Sut)+(0.0000135*Sut**2)-(0.0000000267*Sut**3))/(r**0.5)))
def q_bending(Sut, r=0.1):
	Sut = Sut*0.145
	return 1/(1+((0.246-(0.00308*Sut)+(0.0000151*Sut**2)-(0.0000000267*Sut**3))/(r**0.5)))
#}}}

#Function Goodman{{{
def Goodman(d, Se, Sut, Kf, Kfs, Ma, Tm):
	return (3.1415 * d**3)/(((16/Se)*(4*(Kf*Ma)**2)**0.5) + ((16/Sut)*(3*(Kfs*Tm)**2)**0.5))
#}}}

#Function ASME-Elliptic{{{
def ASME_Elliptic(d, Se, Sy, Kf, Kfs, Ma, Tm):
	return (3.1415 * (d**3))/(16*((4*((Kf*Ma/Se)**2) + 3*((Kfs*Tm/Sy)**2))**0.5))
#}}}

#Function Get_y{{{
#this function returns y for a x, traicing a line between points [x1,y1] and [x2,y2]
def Get_y(x1, y1, x2, y2, x):
	return (((y2-y1)/(x2-x1))*(x-x1))+y1
#}}}

#Function drawShaftInPDF{{{
def drawShaftinPDF(canvas, shaft, stress_points):
	#180x50
	factor = 1

	if shaft.sections[-1][1][0] > 180:
		factor = 180/shaft.sections[-1][1][0]

	for s in shaft.sections:
		canvas.rect(10+s[0][0]*factor, 35-s[0][1]*factor, w=(s[1][0]-s[0][0])*factor, h=s[0][1]*2*factor)

	for p in stress_points:
		canvas.circle(10+p[0]*factor, 35, radius=3, style='FD')
		canvas.text(9+p[0]*factor, 36, text=chr(97+stress_points.index(p)))
#}}}
