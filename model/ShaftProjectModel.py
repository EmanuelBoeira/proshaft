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

	#Clean{{{
	#This method clean the variables to recalculate without keep values
	def Clean(self) -> None:
		self.plot_f_xy.clear()
		self.plot_f_xz.clear()
		self.plot_f_tot.clear()
		self.plot_m_xy.clear()
		self.plot_m_xz.clear()
		self.plot_m_tot.clear()
		self.plot_t.clear()
		self.material.clear()
		self.stress_points.clear()
	#}}}
	#DefineMaterial{{{
	#This function define Sut an Sy for the material passed by
	def DefineMaterial(self, material:str, fabrication_method:str) -> None:
		materials_list = [["Aço 1050(temperado 800°F)", 1090.0, 793.0], ["Aço 1020(laminado a quente)", 379, 207], ["Alíminio", 55, 15], ["Aço 1040(laminado a quente)", 524, 290], ["Aço 1050(laminado a quente)", 621, 345]] 

		for element in materials_list:
			if element[0] == material:
				#print(element)
				self.material = element
				self.material.append(fabrication_method)
				print(self.material)
				break
#}}}
	#GeneratePlots{{{
	def GeneratePlots(self, shaft) -> None:
		#clean the variables and aply initial conditions{{{
		self.plot_f_xy.append([0,0])
		self.plot_f_xz.append([0,0])
		self.plot_m_xy.append([0,0])
		self.plot_m_xz.append([0,0])
		self.plot_t.append([0,0])
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
		#}}}
		#calculate the reactions on supports of shaft{{{
		rxy1 = 0
		rxz1 = 0
		rxy2 = 0
		rxz2 = 0

		#calculate the reactions of the second support
		for force in shaft.forces_xy:
			rxy2 = rxy2 + ((force[0]-shaft.supports[0]) * force[2])
		rxy2 = (-1)*rxy2/(shaft.supports[1]-shaft.supports[0])
		self.plot_f_xy.append([shaft.supports[1], rxy2])

		for force in shaft.forces_xz:
			rxz2 = rxz2 + ((force[0]-shaft.supports[0]) * force[2])
		rxz2 = (-1)*rxz2/(shaft.supports[1]-shaft.supports[0])
		self.plot_f_xz.append([shaft.supports[1], rxz2])

		#calculate the reactions of the first support
		for force in self.plot_f_xy:
			rxy1 = rxy1 + force[1]
	
		for force in self.plot_f_xz:
			rxz1 = rxz1 + force[1]

		self.plot_f_xy.append([shaft.supports[0], (-1)*rxy1])
		self.plot_f_xz.append([shaft.supports[0], (-1)*rxz1])

		#sort the forces in order of x
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
		#from forces in xy
		for i in range(len(self.plot_f_xy)-1):
			if self.plot_f_xy[i+1][0] != self.plot_f_xy[i][0]:
				self.plot_m_xy.append([self.plot_f_xy[i+1][0], self.plot_f_xy[i+1][1]*(self.plot_f_xy[i+1][0]-self.plot_f_xy[i][0])])

		for i in range(len(self.plot_m_xy)-1):
			self.plot_m_xy[i+1][1] = self.plot_m_xy[i][1] + self.plot_m_xy[i+1][1]
		
		#from forces in xz
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
		#Calculate Mtot{{{
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
		#stress_point = [x position, diamiter, Kf, Kfs]
		#add stress concentraton points for flat key and stop ring

		x = 0

		for s in shaft.stress:
			if s[2] == 'flat key':
				self.stress_points.append([s[0]+(s[3][0]/2), s[1], Kf(2.14, q_bending(s[1]/2, self.material[1])), Kfs(3, q_torsion(s[1]/2, self.material[1]))])

			elif s[2] == 'stop ring':
				self.stress_points.append([s[0]+(s[3][0]/2), s[1], Kf(5, q_bending(s[1]/2, self.material[1])), Kfs(3, q_torsion(s[1]/2, self.material[1]))])

		#add stress concetration for diamiter variation
		for i in range(len(shaft.sections)-1):
			x = x + shaft.sections[i][1]
			
			if shaft.sections[i][0] < shaft.sections[i+1][0]:
				kt = Kt(shaft.sections[i+1][0], shaft.sections[i][0])
				kts = Kts(shaft.sections[i+1][0], shaft.sections[i][0])

				self.stress_points.append([x, shaft.sections[i][0], Kf(kt, q_bending(float(self.material[1]))), Kfs(kts, q_torsion(float(self.material[1])))])

				print("q bend: {} Kt: {}".format(q_bending(self.material[1]), kt))
				print("q tors: {} Kts: {}".format( q_torsion(self.material[1]), kts))

			else:
				kt = Kt(shaft.sections[i][0], shaft.sections[i+1][0])
				kts = Kts(shaft.sections[i][0], shaft.sections[i+1][0])

				self.stress_points.append([x, shaft.sections[i+1][0], Kf(kt, q_bending(float(self.material[1]))), Kfs(kts, q_torsion(float(self.material[1])))])

				print("q bend: {} Kt: {}".format(q_bending(self.material[1]), kt))
				print("q tors: {} Kts: {}".format( q_torsion(self.material[1]), kts))

		self.stress_points.sort()
		print(self.stress_points)
		#}}}
	#}}}
	#CalcGoodman{{{
	def CalcGoodman(self) -> None:
	
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
	def CalcASME(self, shaft) -> None:
	
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
			
			for i in range(len(self.plot_t)-1):
				if point[0] >= self.plot_t[i][0] and point[0] < self.plot_t[i+1][0]:
					Tm = self.plot_t[i][1]
	
			#print(point)

			if Ma != 0:
				print('Ma: {} Tm: {}'.format(Ma, Tm))
				nf = ASME_Elliptic(point[1], Se(self.material[1], ka(self.material[1], self.material[3]), kb(point[1]), 1, 1, 0.814, 1), self.material[2], point[2], point[3], Ma, Tm)
			else:
				nf = 0

			results.cell(0,15, 'nf({}) = {}'.format(chr(97+self.stress_points.index(point)), nf), ln=2)

		drawShaftinPDF(results, shaft, self.stress_points)
		results.output("eixo.pdf")

		webbrowser.open('eixo.pdf')
	#}}}
#}}}

#Function Se{{{
#function to calculate fatigue endurance limit.
def Se(Sut, ka=1, kb=1, kc=1, kd=1, ke=1, kf=1) -> float:
	return (0.5*Sut)*ka*kb*kc*kd*ke*kf
#}}}

#Function ka{{{
#function to calculate factor  ka.
def ka(Sut:float, factory:str='Usinado') -> float:

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
def kb(d:float) -> float:
	if d <= 51 and d >= 2.8:
		return 1.24*(d**(-0.107))
	elif d > 51 and d <= 254:
		return 1.51 * (d*(-0.157))
	else:
		return 0
#}}}

#Function kd{{{
def kd(temp:float) -> float:
	temp = (temp*1.8)+32

	return 0.975+(0.000432*temp)-(0.00000115*(temp**2))+(0.00000000104*(temp**3))-(0.000000000000595*(temp**4))
#}}}

#Function ke{{{
def ke(conf:float) -> float:
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

#Functions Kt and Kts{{{
def Kt(D:float, d:float, r:float=4) -> float:
	t = (D - d)/2
	C1 = 0.947 + 1.206*(t/r)**0.5 - 0.131*(t/r)
	C2 = 0.022 - 3.405*(t/r)**0.5 + 0.915*(t/r)
	C3 = 0.869 + 1.777*(t/r)**0.5 - 0.555*(t/r)
	C4 = -0.81 + 0.422*(t/r)**0.5 - 0.260*(t/r)

	return C1 + C2*(2*t/D) + C3*(2*t/D)**2 + C4*(2*t/D)**3

def Kts(D:float, d:float, r:float=4) -> float:
	t = (D - d)/2
	C1 =  0.905 + 0.783*(t/r)**0.5 - 0.075*(t/r)
	C2 = -0.437 - 1.969*(t/r)**0.5 + 0.553*(t/r)
	C3 =  1.557 + 1.073*(t/r)**0.5 - 0.578*(t/r)
	C4 = -1.061 + 0.171*(t/r)**0.5 - 0.086*(t/r)

	return C1 + C2*(2*t/D) + C3*(2*t/D)**2 + C4*(2*t/D)**3
#}}}

#Function Kf{{{
def Kf(Kt:float, q:float) -> float:
	return 1+(q*(Kt-1))
#}}}

#Function Kfs{{{
def Kfs(Kts:float, q:float) -> float:
	return 1+(q*(Kts-1))
#}}}

#Functions q{{{
#r é o raio do entalhe (entre 0 e 4 mm). Sut deve estar em MPa que é convertido em kpsi
def q_torsion(Sut:float, r:float=0.16) -> float:
	Sut = Sut*0.145
	return 1/(1+((0.19-(0.00251*Sut)+(0.0000135*Sut**2)-(0.0000000267*Sut**3))/(r**0.5)))
def q_bending(Sut:float, r:float=0.16) -> float:
	Sut = Sut*0.145
	return 1/(1+((0.246-(0.00308*Sut)+(0.0000151*Sut**2)-(0.0000000267*Sut**3))/(r**0.5)))
#}}}

#Function Goodman{{{
def Goodman(d, Se, Sut, Kf, Kfs, Ma, Tm) -> float:
	return (3.1415 * d**3)/(((16/Se)*(4*(Kf*Ma)**2)**0.5) + ((16/Sut)*(3*(Kfs*Tm)**2)**0.5))
#}}}

#Function ASME-Elliptic{{{
def ASME_Elliptic(d, Se, Sy, Kf, Kfs, Ma, Tm) -> float:
	return (3.1415 * (d**3))/(16*((4*((Kf*Ma/Se)**2) + 3*((Kfs*Tm/Sy)**2))**0.5))
#}}}

#Function Get_y{{{
#this function returns y for a x, traicing a line between points [x1,y1] and [x2,y2]
def Get_y(x1:float, y1:float, x2:float, y2:float, x:float) -> float:
	return (((y2-y1)/(x2-x1))*(x-x1))+y1
#}}}

#Function drawShaftInPDF{{{
def drawShaftinPDF(canvas, shaft, stress_points) -> None:
	#180x50
	factor = 1
	length = 0

	for section in shaft.sections:
		length = length + section[1]

	if length > 180:
		factor = 180/length

	length = 0

	for s in shaft.sections:
		canvas.rect(10+(length)*factor, 35-s[0]*factor/2, w=(s[1])*factor, h=s[0]*factor)
		length = length + s[1]

	for p in stress_points:
		canvas.circle(10+p[0]*factor, 35, radius=3, style='FD')
		canvas.text(9+p[0]*factor, 36, text=chr(97+stress_points.index(p)))
#}}}
