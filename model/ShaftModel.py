#mathematic model for shaft project.
#Class Shaft {{{
#class for a shaft object.
class Shaft: 
	sections = []    #sections, [[x1,y1], [x2,y2]]
	supports = []    #distance x of the 2 supports
	forces_xy = []   #forces in the shaft in plane xy [x, y, F]
	forces_xz = []   #forces in the shaft in plane xz [x, y, F]
	moments_xy = []  #moments in plane xy [x,m]
	moments_xz = []  #moments in plane xz [x,m]
	stress = []      #list of stress concentrations in the shaft [x, type, [variables]]

	#constructor of the class shaft.
	def __init__(self):
		self.supports = [0,0]

	#method to add a section to the list sections
	#AddSection{{{
	def AddSection(self, x1, y1, x2, y2):
		self.sections.append([[x1,y1],[x2,y2]])
		self.sections.sort()
	#}}}

    #method to remove a section from the list sections.
	#RemovaSection{{{
	def RemoveSection(self, i):
		for f in self.forces_xy:
			if f[0] > self.sections[i][1][0]:
				self.forces_xy.remove(f)

		for f in self.forces_xz:
			if f[0] > self.sections[i][1][0]:
				self.forces_xz.remove(f)

		self.sections.remove(self.sections[i])

		for s in self.stress:
			if s[0] > self.sections[i][1][0]:
				self.stress.remove(s)
	#}}}

    #method to add a position of a support in the list supports.
	#AddSupport{{{
	def AddSupport(self, x, i):
		self.supports[i] = x
	#}}}

    #method to add a force to list forces. x is the x coordenate, y_or_z is the y or z coordenate, tangential is bool value (True if is tangential), plane_xy is a bool value (True if is in xy) and F is the magnitude.
	#AddForce{{{
	def AddForce(self, x, y_or_z, tangential, plane_xy, F):
		if tangential:
			if plane_xy:
				self.forces_xz.append([x, y_or_z, F])
			elif not plane_xy:
				self.forces_xy.append([x, y_or_z, F])
		#for radial forces, y or z doesn't matters
		else:
			if plane_xy:
				self.forces_xy.append([x, 0, F])
			else:
				self.forces_xz.append([x, 0, F])

		self.forces_xy.sort()
		self.forces_xz.sort()
	#}}}

    #method to remove a force from the list forces.
	#RemoveForce{{{
	def RemoveForce(self, i, plane_xy):
		if plane_xy:
			self.forces_xy.remove(self.forces_xy[i])
		else:
			self.forces_xz.remove(self.forces_xz[i])
	#}}}

	#AddStress{{{
	def AddStress(self, stress, variables):
		self.stress.append([stress, variables])
		self.stress.sort()
	#}}}

	#RemoveStress{{{
	def RemoveStress(self, i):
		self.stress.remove(self.stress[i])
	#}}}

	#AddMoment{{{
	def AddMoment(self, x, m, plane_xy):
		if plane_xy:
			self.moments_xy.append([x, m])
		else:
			self.moments_xz.append([x, m])
	#}}}
#}}}

#Function Reaction {{{
#function to calculate reactions in 2 supports in a shaft s.
def Reactions(s): 
	rxy1 = 0
	rxz1 = 0
	rxy2 = 0
	rxz2 = 0

	#calculate the reactions of the second support.
	for force in s.forces_xy:
		rxy2 = rxy2 + ((force[0]-s.supports[0]) * force[2])
	rxy2 = (-1)*rxy2/(s.supports[1]-s.supports[0])
	s.AddForce(s.supports[1], 0, False, True, rxy2)

	for force in s.forces_xz:
		rxz2 = rxz2 + ((force[0]-s.supports[0]) * force[2])
	rxz2 = (-1)*rxz2/(s.supports[1]-s.supports[0])
	s.AddForce(s.supports[1], 0, False, False, rxz2)

	#calculate the reactions of the first support.
	for force in s.forces_xy:
		rxy1 = rxy1 + force[2]
	
	for force in s.forces_xz:
		rxz1 = rxz1 + force[2]

	s.AddForce(s.supports[0], 0, False, True, (-1)*rxy1)
	s.AddForce(s.supports[0], 0, False, False, (-1)*rxz1)

	#sort the forces in order of x.
	s.forces_xy.sort()
	s.forces_xz.sort()
#}}}

#Function Bending_Moment{{{
#function to calculate bending moment to a shaft s.
def Bending_Moment(s):
	fxy = []
	fxz = []

	#separete forces by plane.
	for f in s.forces_xy:
		fxy.append([f[0], f[2]])

	for f in s.forces_xz:
		fxz.append([f[0], f[2]])

	#calculate the distance between each point and sum forces.
	for i in range(len(fxy)):
		if i+1 < len(fxy):
			fxy[i+1][1] = fxy[i+1][1] + fxy[i][1]
			fxy[i][0] = fxy[i+1][0] - fxy[i][0]

	for i in range(len(fxz)):
		if i+1 < len(fxz):
			fxz[i+1][1] = fxz[i+1][1] + fxz[i][1]
			fxz[i][0] = fxz[i+1][0] - fxz[i][0]

	#multiplicate force by distance(integral by area).
	for f in fxy:
		s.AddMoment(f[0], f[0]*f[1], True)

	for f in fxz:
		s.AddMoment(f[0], f[0]*f[1], False)
	
	for i in range(len(s.forces_xy)-1):
		s.moments_xy[i][0] = s.forces_xy[i+1][0]
		s.moments_xy[i+1][1] = s.moments_xy[i][1] + s.moments_xy[i+1][1]

	s.moments_xy.remove(s.moments_xy[-1])

	for i in range(len(s.forces_xz)-1):
		s.moments_xz[i][0] = s.forces_xz[i+1][0]
		s.moments_xz[i+1][1] = s.moments_xz[i][1] + s.moments_xz[i+1][1]

	s.moments_xz.remove(s.moments_xz[-1])

	#sum the moments.
	#for i in range(len(mxy)-1):
	#	mxy[i+1] = mxy[i] + mxy[i+1]
	#for i in range(len(mxz)-1):
	#	mxz[i+1] = mxz[i] + mxz[i+1]
	
	#calculate the total moment.
	#for i in range(len(mxy)-1):
	#	s.AddMoment(float(((mxy[i]**2) + (mxz[i])**2)**0.5)/1000)
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

