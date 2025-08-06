#section to add a section for shaft project
#adicionar img
import tkinter as tk
import tkinter.ttk as ttk

class ShaftSectionWindow:
	def __init__(self, origin, controller):
		#tk instance
		self.root = tk.Toplevel(origin)
		self.controller = controller

		#window atributes
		self.root.title('Adicionar seção')
		self.root.geometry('500x300')
		self.root.resizable(False, False)

		#root elements.
		self.text1 = tk.Label(self.root, text='D(mm):')
		self.text1.place(x=30, y=80)

		self.d = tk.Entry(self.root, width=100)
		self.d.place(x=100, y=80, width=100)

		self.text2 = tk.Label(self.root, text='L(mm):')
		self.text2.place(x=30, y=140)

		self.l = tk.Entry(self.root, width=100)
		self.l.place(x=100, y=140, width=100)

		self.buttonAddSection = tk.Button(self.root, text='Adicionar', command =lambda: [self.AddSection(), self.controller.UpdateSectionTreeview(), self.controller.UpdateCanvas(), self.root.destroy()])
		self.buttonAddSection.place(x=220, y=240, width=120, height=30)

		self.buttonCancel = tk.Button(self.root, text='Cancelar', command = self.root.destroy)
		self.buttonCancel.place(x=360, y=240, width=120, height=30)

	#def SetController(self, controller):
	#	self.controller = controller

	def AddSection(self):
		self.controller.AddSectionToModel(0, (float(self.d.get())/2), float(self.l.get()), (float(self.d.get())/2))
