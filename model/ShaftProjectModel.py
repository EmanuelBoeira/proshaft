#class for Shaft Project{{{
class ShaftProject:
	plot_f_xy  =  [[0,0]]
	plot_f_xz  =  [[0,0]]
	plot_f_tot =  []
	plot_m_xy  =  [[0,0]]
	plot_m_xz  =  [[0,0]]
	plot_m_tot =  []
	plot_t     =  [[0,0]]
	material   =  ''

	#init{{{
	def __init__(self, shaft):
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

		#adicionar Ftot aqui
		for i in range(len(self.plot_f_xy)):
			self.plot_f_tot.append([self.plot_f_xy[i][0], ((self.plot_f_xy[i][1]**2)+(self.plot_f_xz[i][1]**2))**0.5])
			
		#adicionar Mtot aqui
		for i in range(len(self.plot_m_xy)):
			self.plot_m_tot.append([self.plot_m_xy[i][0], ((self.plot_m_xy[i][1]**2)+(self.plot_m_xz[i][1]**2))**0.5])
			
	#}}}

	#clean the values{{{
	def Clean(self):
		plot_f_xy  =  [[0,0]]
		plot_f_xz  =  [[0,0]]
		plot_f_tot =  [[0,0]]
		plot_m_xy  =  [[0,0]]
		plot_m_xz  =  [[0,0]]
		plot_m_tot =  [[0,0]]
		plot_t     =  [[0,0]]
		material   =  ''
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
def Kf(stress, val, q):
	#list of stresses. [stress, Kt, Kts, value for selection]
	stress_list = [['diameter', 2.7, 2.2, 0.02], ['diameter', 1.7, 1.5, 0.1], ['flat key', 2.14, 3, 0.02], ['stop ring', 5, 3, 0]]

	for s in stress_list:
		if s == stress:
			return 1+(q*(s[1]-1))
			break
	
	return 0
#}}}

#Function Kfs{{{
def Kf(stress, val, q):
	#list of stresses. [stress, Kt, Kts, value for selection]
	stress_list = [['diameter', 2.7, 2.2, 0.02], ['diameter', 1.7, 1.5, 0.1], ['flat key', 2.14, 3, 0.02], ['stop ring', 5, 3, 0]]

	for s in stress_list:
		if s == stress:
			return 1+(q*(s[2]-1))
			break
	
	return 0
#}}}

#Function q{{{
def q(t, r, Sut):
	if t == 'torsion':
		return 1/(1+((0.246-(0.00308*Sut)+(0.0000151*Sut**2)-(0.0000000267*Sut**3))/(r**0.5)))
	elif t == 'bending':
		return 1/(1+((0.19-(0.00251*Sut)+(0.0000135*Sut**2)-(0.0000000267*Sut**3))/(r**0.5)))
	else:
		return 0
#}}}
