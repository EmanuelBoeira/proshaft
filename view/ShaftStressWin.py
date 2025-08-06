#window for add caracteristcs of strees concentration for shaft project
#adicionar tudo 
import tkinter as tk

class ShaftStressWindow:
	def __init__(self, origin, controller):
		#instancia de tk.
		self.root = tk.Toplevel(origin)
		self.controller = controller

		#atributos da janela.
		self.root.title('Adicionar força')
		self.root.geometry('500x300')
		self.root.resizable(False, False)

		#elementos de root.
		button_add_stress = tk.Button(self.root, text='Adicionar')
		button_add_stress.place(x=220, y=240, width=120, height=30)

		button_cancel = tk.Button(self.root, text='Cancelar', command = self.root.destroy)
		button_cancel.place(x=360, y=240, width=120, height=30)
