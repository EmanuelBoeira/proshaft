#window for add caracteristcs of strees concentration for shaft project
#adicionar tudo 
import tkinter as tk
import tkinter.ttk as ttk

#Class ShaftStressWindow{{{
class ShaftStressWindow:
	def __init__(self, origin, controller):
		#instancia de tk.
		self.root = tk.Toplevel(origin)
		self.controller = controller
		
		#atributos da janela.{{{
		self.root.title('Adicionar força')
		self.root.geometry('500x320')
		self.root.resizable(False, False)
		#}}}

		#elementos de root.{{{
		stress_list = ['flat key','stop ring']
		self.stress = tk.StringVar()
		self.combo_box_stress = ttk.Combobox(self.root, textvariable=self.stress, values=stress_list, state='readonly')
		self.combo_box_stress.place(x=10, y=10, width=250, height=30)
		self.combo_box_stress.bind('<<ComboboxSelected>>', self.SwitchFrame)

		self.frame_default = ttk.Labelframe(self.root, text='Stress', width=480, height=200)
		self.frame_default.place(x=10, y=50)

		self.frame_flat_key = ttk.Labelframe(self.root, text='Chaveta', width=480, height=200)

		self.frame_stop_ring = ttk.Labelframe(self.root, text='Anel de retenção', width=480, height=200)

		button_add_stress = tk.Button(self.root, text='Adicionar', command = self.AddStress)
		button_add_stress.place(x=220, y=270, width=120, height=30)

		button_cancel = tk.Button(self.root, text='Cancelar', command = self.root.destroy)
		button_cancel.place(x=360, y=270, width=120, height=30)
		#}}}

		#frame_flat_key elements{{{
		text1 = ttk.Label(self.frame_flat_key, text='x(mm):')
		text1.place(x=10, y=10)

		self.x = ttk.Entry(self.frame_flat_key)
		self.x.place(x=60, y=10, width=100)

		text2 = ttk.Label(self.frame_flat_key, text='l(mm):')
		text2.place(x=10, y=40)

		self.l = ttk.Entry(self.frame_flat_key)
		self.l.place(x=60, y=40, width=100)

		text3 = ttk.Label(self.frame_flat_key, text='b(mm):')
		text3.place(x=10, y=70)

		self.b = ttk.Entry(self.frame_flat_key)
		self.b.place(x=60, y=70, width=100)
		#}}}

		#frame_stop_ting elements

	#Function SwitchFrame{{{
	def SwitchFrame(self, event):
		if self.stress.get() == 'flat key':
			self.frame_flat_key.place(x=10, y=50)
			self.frame_default.place_forget() if self.frame_default.winfo_ismapped() else self.frame_stop_ring.place_forget()

		if self.stress.get() == 'stop ring':
			self.frame_stop_ring.place(x=10, y=50)
			self.frame_default.place_forget() if self.frame_default.winfo_ismapped() else self.frame_flat_key.place_forget()
	#}}}

	def AddStress(self):
		if self.stress.get() == 'flat key':
			self.controller.AddStressToModel(self.stress.get(), float(self.x.get()), float(self.l.get()), float(self.b.get()))
			self.controller.UpdateCanvas()
			self.controller.UpdateSectionTreeview()
			self.root.destroy()
		else:
			self.root.destry()
#}}}
