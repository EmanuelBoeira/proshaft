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
	#RemoveSection{{{
	def RemoveSection(self, i):
		for f in self.forces_xy:
			if f[0] > self.sections[i][1][0]:
				self.forces_xy.remove(f)

		for f in self.forces_xz:
			if f[0] > self.sections[i][1][0]:
				self.forces_xz.remove(f)

		for s in self.stress:
			if s[0] > self.sections[i][1][0]:
				self.stress.remove(s)

		self.supports[1] = self.sections[i][0][0]
		self.sections.remove(self.sections[i])
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

