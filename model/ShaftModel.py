#Class Shaft {{{
#class for a shaft object.
class Shaft: 
	sections  = []  #sections [Diamiter, Length]
	supports  = []  #distance x of the 2 supports
	forces_xy = []  #forces on shaft in plane xy [x, y, F]
	forces_xz = []  #forces on shaft in plane xz [x, y, F]
	stress    = []  #list of stress concentrations [x position, diamiter, type, [variables]]

	#constructor of the class shaft.
	def __init__(self):
		self.supports = [0,0]

	#AddSection{{{
	#method to add a section to the list sections
	def AddSection(self, Diamiter, Length):
		self.sections.append([Diamiter, Length])
	#}}}
	#RemoveSection{{{
    #method to remove a section from the list sections.
	def RemoveSection(self, index):
		self.sections.remove(self.sections[index])
	#}}}
	#ModifySection{{{
	def ModifySection(self, index, newDiamiter, newLength):
		self.sections[index] = [newDiamiter, newLength]
	#}}}
	#ModifySupport{{{
    #method to add a position of a support in the list supports.
	def ModifySupport(self, x, index):
		self.supports[index] = x
	#}}}
	#AddForce{{{
    #method to add a force to list forces. 
	#x is the x coordenate, 
	#y_or_z is the y or z coordenate, 
	#plane_xy is a bool value (True if is in xy) 
	#and F is the magnitude.
	def AddForce(self, x, y_or_z, plane_xy, F):
		if plane_xy:
			self.forces_xy.append([x, y_or_z, F])
		else:
			self.forces_xz.append([x, y_or_z, F])

		self.forces_xy.sort()
		self.forces_xz.sort()
	#}}}
	#RemoveForce{{{
    #method to remove a force from the list forces.
	def RemoveForce(self, index, plane_xy):
		if plane_xy:
			self.forces_xy.remove(self.forces_xy[index])
		else:
			self.forces_xz.remove(self.forces_xz[index])
	#}}}
	#AddStress{{{
	def AddStress(self, x, diamiter, stress, variables):
		self.stress.append([x, diamiter, stress, variables])
		self.stress.sort()
	#}}}
	#RemoveStress{{{
	def RemoveStress(self, index):
		self.stress.remove(self.stress[index])
	#}}}
#}}}
