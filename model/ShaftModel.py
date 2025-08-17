#mathematic model for shaft project.
#Class Shaft {{{
#class for a shaft object.
class Shaft: 
	sections = [] #sections, [raio, comprimento]
	supports = [] #distance x of the 2 supports
	forces = []   #forces in the shaft
	mtot = []     #points of total moment to make the grafic
	stress = []   #list of stress concentrations in the shaft [type, x, l]

	#constructor of the class shaft.
	def __init__(self):
		self.supports = [0,0]

	#method to add a section to the list sections
	def AddSection(self, x1, y1, x2, y2):
		self.sections.append([[x1,y1],[x2,y2]])
		self.sections.sort()

    #method to remove a section from the list sections.
	def RemoveSection(self, i):
		self.sections.remove(self.sections[i])

    #method to add a position of a support in the list supports.
	def AddSupport(self, x, i):
		self.supports[i] = x

    #method to remove support from the list supports.
	def RemoveSupport(self, i):
		self.supports.remove(self.supports[i])

    #method to add a force to list forces. x is the x coordenate, y_or_z is the y or z coordenate, tangential is bool value (True if is tangential), plane_xy is a bool value (True if is in xy) and F is the magnitude.
	def AddForce(self, x, y_or_z, tangential, plane_xy, F):
		if tangential:
			if plane_xy:
				self.forces.append([x, y_or_z, tangential, False, F])
			elif not plane_xy:
				self.forces.append([x, y_or_z, tangential, True, F])
		#for radial forces, y or z doesn't matters
		else:
			self.forces.append([x, 0, tangential, plane_xy, F])
		self.forces.sort()

    #method to remove a force from the list forces.
	def RemoveForce(self, i):
		self.forces.remove(self.forces[i])

	def AddStress(self, x, l, b, stress):
		self.stress.append([x, l, b, stress])
		self.stress.sort()

	def RemoveStress(self, i):
		self.stress.remove(self.stress[i])

	def AddMoment(self, m):
		self.mtot.append(m)
#}}}

#Function Reaction {{{
#function to calculate reactions in 2 supports in a shaft s.
def Reactions(s): 
	xy = []
	xz = []
	rxy1 = 0
	rxz1 = 0
	rxy2 = 0
	rxz2 = 0

	#add info needed for calculate the reactions in the second support(sum of momentum equals zero).
	for force in s.forces:
		if force[0] < s.supports[0]:
			force[4] = -force[4]

		if force[3]:
			xy.append([force[0], force[4]])
		else:
			xz.append([force[0], force[4]])
	
	#calculate the reactions of the second support.
	for force in xy:
		rxy2 = rxy2 + (force[0] * force[1])
	rxy2 = (-1)*rxy2/s.supports[1]
	s.AddForce(s.supports[1], 0, False, True, rxy2)

	for force in xz:
		rxz2 = rxz2 + (force[0] * force[1])
	rxz2 = (-1)*rxz2/s.supports[1]
	s.AddForce(s.supports[1], 0, False, False, rxz2)

	#calculate the reactions of the first support.
	for force in s.forces:
		if force[3]:
			rxy1 = rxy1 + force[4]
		if not force[3]:
			rxz1 = rxz1 + force[4]
	s.AddForce(s.supports[0], 0, False, True, (-1)*rxy1)
	s.AddForce(s.supports[0], 0, False, False, (-1)*rxz1)

	#sort the forces in order of x.
	s.forces.sort()
#}}}

#Function Bending_Moment{{{
#function to calculate bending moment to a shaft s.
def Bending_Moment(s):
	fxy = []
	fxz = []
	mxy = []
	mxz = []

	#separete forces by plane.
	for f in s.forces:
		if f[3]:
			fxy.append([f[0], f[4]])
		if not f[3]:
			fxz.append([f[0], f[4]])

	#print(fxy)

	#calculate the distance between each point and sum forces.
	for i in range(len(fxy)):
		if i+1 < len(fxy):
			fxy[i+1][1] = fxy[i+1][1] + fxy[i][1]
			fxy[i][0] = fxy[i+1][0] - fxy[i][0]

	fxy.remove(fxy[-1])

	for i in range(len(fxz)):
		if i+1 < len(fxz):
			fxz[i+1][1] = fxz[i+1][1] + fxz[i][1]
			fxz[i][0] = fxz[i+1][0] - fxz[i][0]

	fxz.remove(fxz[-1])

	#print(fxy)

	#multiplicate force by distance(integral by area).
	for f in fxy:
		mxy.append(f[0] * f[1])
	for f in fxz:
		mxz.append(f[0] * f[1])

	#sum the moments.
	for i in range(len(mxy)-1):
		mxy[i+1] = mxy[i] + mxy[i+1]
		mxz[i+1] = mxz[i] + mxz[i+1]
	
	#calculate the total moment.
	for i in range(len(mxy)-1):
		s.AddMoment(float(((mxy[i]**2) + (mxz[i])**2)**0.5)/1000)
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

#Function dmin_VonMisses{{{
#function to calculate minimum diamiter by Von Misses.
def dmin_VonMisses(nf, Kf, Kfs, Ma, Tm, Se, Sy):
	return ((16*nf/3.1415)*(((4*((Kf*Ma/Se)**2))+(3*((Kfs*Tm/Sy)**2)))**(0.5)))**(1/3)
#}}}

#exemplo:
#shaft1 = Shaft()
#shaft1.AddSection(0,10,250,10)
#shaft1.AddSection(250,20,260,20)
#shaft1.AddForce(50, 10, 'r', 'xy', -876)
#shaft1.AddForce(50, 10, 'r', 'xz', 2400)
#shaft1.AddForce(195, 10, 'r', 'xy', -3937)
#shaft1.AddForce(195, 10, 'r', 'xz', -10814)
#shaft1.AddSupport(0)
#shaft1.AddSupport(250)

