#class for Shaft Project{{{
class ShaftProject:
	plot_f_xy  =  []
	plot_f_xz  =  []
	plot_f_tot =  []
	plot_m_xy  =  []
	plot_m_xz  =  []
	plot_m_tot =  []
	plot_t     =  []
	material   =  [] # [material, Sut, Sy, Surface Factor]
	stress_points = []

	#init{{{
	def __init__(self, shaft, mat, fac):
		self.plot_f_xy.append([0,0])
		self.plot_f_xz.append([0,0])
		self.plot_m_xy.append([0,0])
		self.plot_m_xz.append([0,0])
		self.plot_t.append([0,0])

		self.material.clear()
		if mat == "Aço 1050":
			self.material.append(mat)
			self.material.append(1090)
			self.material.append(793)
			self.material.append(fac)

		#add forces and torque from the shaft
		for f in shaft.forces_xy:
			self.plot_f_xy.append([f[0], f[2]])

			if f[1] != 0:
				self.plot_t.append([f[0], f[1]*f[2]])

		for f in shaft.forces_xz:
			self.plot_f_xz.append([f[0], f[2]])

			if f[1] != 0:
				self.plot_t.append([f[0], f[1]*f[2]])

		#calculate the reactions on supports of shaft{{{
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

		#Calculate Ftot
		for i in range(len(self.plot_f_xy)):
			self.plot_f_tot.append([self.plot_f_xy[i][0], ((self.plot_f_xy[i][1]**2)+(self.plot_f_xz[i][1]**2))**0.5])
			
		#calculate Mtot
		for i in range(len(self.plot_m_xy)):
			self.plot_m_tot.append([self.plot_m_xy[i][0], ((self.plot_m_xy[i][1]**2)+(self.plot_m_xz[i][1]**2))**0.5])
			
		#adicionar pontos de interesse em stress_points
		for s in shaft.stress:
			self.stress_points.append([s[0]+(s[3][0]/2), s[1], Kf(s[2], q_bending(s[1]/2, self.material[1])), Kfs(s[2], q_torsion(s[1]/2, self.material[1]))])

		for i in range(len(shaft.sections)-1):
			if shaft.sections[i][1][1] < shaft.sections[i+1][0][1]:
				self.stress_points.append([shaft.sections[i][1][0], shaft.sections[i][1][1]*2, Kf('diameter-0.02', q_bending(self.material[1]/1000)), Kfs('diameter-0.02', q_torsion(self.material[1]/1000))])
			else:
				self.stress_points.append([shaft.sections[i+1][0][0], shaft.sections[i][0][1]*2, Kf('diameter-0.02', q_bending(self.material[1]/1000)), Kfs('diameter-0.02', q_torsion(self.material[1]/1000))])

		self.stress_points.sort()
		print(self.stress_points)
	#}}}

	#clean{{{
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

	#SetMaterial{{{
	def SetMaterial(self, m, f):
		self.material.clear()
		if m == "Aço 1050":
			self.material.append(m)
			self.material.append(1090)
			self.material.append(793)
			self.material.append(f)
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
			print(point)
			print(Goodman(point[1], Se(self.material[1], ka(self.material[1], 4.51, -0.265), kb(point[1]), 1, 1, 1, 1), self.material[1], point[2], point[3], Ma, Tm))
		#return Goodman(d, Se(self.material[1], ka(self.material[1], 4.51, -0.265), kb(d), 1, 1, 1, 1), self.material[1], Kf, Kfs, Ma, Tm)
	#}}}
	#CalcASME{{{
	def CalcASME(self):
	
		Ma = 0
		Tm = 0

		for point in self.stress_points:
			for i in range(len(self.plot_m_tot)-1):
				if point[0] >= self.plot_m_tot[i][0] and point[0] < self.plot_m_tot[i+1][0]:
					Ma = Get_y(self.plot_m_tot[i][0], self.plot_m_tot[i][1], self.plot_m_tot[i+1][0], self.plot_m_tot[i+1][1], point[0])
					#break
					print(Get_y(self.plot_m_tot[i][0], self.plot_m_tot[i][1], self.plot_m_tot[i+1][0], self.plot_m_tot[i+1][1], point[0]))
			
			for i in range(len(self.plot_t)-1):
				if point[0] >= self.plot_t[i][0] and point[0] < self.plot_t[i+1][0]:
					Tm = self.plot_t[i][1]
					#break

			print(point)
			print(ASME_Elliptic(point[1], Se(self.material[1], ka(self.material[1], 4.51, -0.265), kb(point[1]), 1, 1, 0.814, 1), self.material[2], point[2], point[3], Ma, Tm))
	#}}}
#}}}

#Function Se{{{
#function to calculate fatigue endurance limit.
def Se(Sut, ka, kb, kc, kd, ke, kf):
	return (0.5*Sut)*ka*kb*kc*kd*ke*kf
#}}}

#function ka{{{
#function to calculate factor  ka.
def ka(Sut, x, y):
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

#Function q{{{
#r é o raio do entalhe (entre 0 e 4 mm). Sut deve estar em GPa
def q_bending(Sut, r=0.1):
	return 1/(1+((0.19-(0.00251*Sut)+(0.0000135*Sut**2)-(0.0000000267*Sut**3))/(r**0.5)))
def q_torsion(Sut, r=0.1):
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
