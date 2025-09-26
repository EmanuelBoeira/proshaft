#main window for shaft project
#arrumar posições e textos :(
#imports{{{
import tkinter as tk
import tkinter.ttk as ttk
import ShaftSectionWin as SecWin
import ShaftStressWin as StrWin
import ShaftForceWin as ForWin
import ShaftSupportWin as SupWin
#}}}

#class ShaftMainWindow{{{
class ShaftMainWindow:
	def __init__(self):
		#tk instance
		self.root = tk.Tk()
		self.controller = None

		#window atributes
		self.root.geometry('700x650')
		self.root.title('proshaft')
		self.root.resizable(False, False)

		#root elements{{{
		self.canvas_axial = tk.Canvas(self.root, width=250, height=250, bg='white')
		self.canvas_axial.place(x=10, y=10)

		self.canvas_long = tk.Canvas(self.root, width=420, height=250, bg='white')
		self.canvas_long.place(x=270, y=10)

		self.frame_draw = ttk.Labelframe(self.root, text='Seções:', width=680, height=325)
		self.frame_draw.place(x=10, y=270)

		self.frame_calc = ttk.Labelframe(self.root, text='Forças:', width=680, height=325)

		self.frame_plots = ttk.Labelframe(self.root, text='Gráficos', width=680, height=325)

		self.button_next = ttk.Button(self.root, text='Próximo', command = lambda: self.SwitchFrames(True))
		self.button_next.place(x=570, y=610, width=120, height=30)

		self.button_back = ttk.Button(self.root, text='Voltar', command = lambda: self.SwitchFrames(False))
		self.button_back.place(x=440, y=610, width=120, height=30)

		self.button_cancel = ttk.Button(self.root, text='Cancelar', command = self.root.quit)
		self.button_cancel.place(x=310, y=610, width=120, height=30)
		#}}}

		#frame_draw elements{{{
		self.tree_sections = ttk.Treeview(self.frame_draw)
		self.tree_sections.place(x=5, y=0, width=330, height=260)
		treeviewScroll1 = tk.Scrollbar(self.tree_sections, orient=tk.VERTICAL)
		treeviewScroll1.pack(side=tk.RIGHT, fill=tk.Y)

		button_open_section_win = ttk.Button(self.frame_draw, text='Add section', command=self.OpenSectionWin)
		button_open_section_win.place(x=5, y=270, width=160, height=25)

		button_remove_section = ttk.Button(self.frame_draw, text='Remove section', command = lambda :[self.RemoveSection(), self.controller.UpdateSectionTreeview(),self.controller.UpdateCanvas()])
		button_remove_section.place(x=175, y=270, width=160, height=25)

		self.tree_stress = ttk.Treeview(self.frame_draw)
		self.tree_stress.place(x=345, y=0, width=330, height=260)
		treeviewScroll3 = tk.Scrollbar(self.tree_stress, orient=tk.VERTICAL)
		treeviewScroll3.pack(side=tk.RIGHT, fill=tk.Y)

		button_open_stress_win = ttk.Button(self.frame_draw, text='Add stress', command=self.OpenStressWin)
		button_open_stress_win.place(x=345, y=270, width=160, height=25)

		button_remove_stress = ttk.Button(self.frame_draw, text='Remove stress', command = lambda :[self.RemoveStress(), self.controller.UpdateStressTreeview(), self.controller.UpdateCanvas()])
		button_remove_stress.place(x=515, y=270, width=160, height=25)
		#}}}

		#frame_calc elements{{{
		self.tree_forces = ttk.Treeview(self.frame_calc)
		self.tree_forces.place(x=5, y=0, width=330, height=260)
		treeviewScroll2 = tk.Scrollbar(self.tree_forces, orient=tk.VERTICAL)
		treeviewScroll2.pack(side=tk.RIGHT, fill=tk.Y)

		button_open_force_win = ttk.Button(self.frame_calc, text='Add force', command=self.OpenForceWin)
		button_open_force_win.place(x=350, y=200, width=150, height=25)

		button_remove_force = ttk.Button(self.frame_calc, text='Remove force', command = lambda: [self.RemoveForce(), self.controller.UpdateForceTreeview(), self.controller.UpdateCanvas()])
		button_remove_force.place(x=510, y=200, width=150, height=25)

		button_open_support_win = ttk.Button(self.frame_calc, text='Editar suporte', command=self.OpenSupportWin)
		button_open_support_win.place(x=350, y=235, width=310, height=25)
		#}}}

		#frame_plots elements{{{

		self.listbox_plots = tk.Listbox(self.frame_plots)
		self.listbox_plots.insert(1, 'F(XY)')
		self.listbox_plots.insert(2, 'F(XZ)')
		self.listbox_plots.insert(3, 'F(TOT)')
		self.listbox_plots.insert(4, 'M(XY)')
		self.listbox_plots.insert(5, 'M(XZ)')
		self.listbox_plots.insert(6, 'M(TOT)')
		self.listbox_plots.insert(7, 'Torque')
		self.listbox_plots.place(x=0, y=5, width=130, height=290)

		self.listbox_plots.bind('<<ListboxSelect>>', self.DrawPlot)

		self.canvas_plots = tk.Canvas(self.frame_plots, width=540, height=290, bg='white')
		self.canvas_plots.place(x=130, y=5)

		#}}}

	def SetController(self, controller):
		self.controller = controller

	def SwitchFrames(self, go_next):
		if(go_next):
			if(self.frame_draw.winfo_ismapped()):
				self.frame_calc.place(x=10, y=270)
				self.frame_draw.place_forget()
			elif(self.frame_calc.winfo_ismapped()):
				self.frame_plots.place(x=10, y=270)
				self.frame_calc.place_forget()
				print('calculando...')
				self.controller.CalculateShaft()
			elif(self.frame_plots.winfo_ismapped()):
				print('gerar pdf...')
		else:
			if(self.frame_calc.winfo_ismapped()):
				self.frame_draw.place(x=10, y=270)
				self.frame_calc.place_forget()
			elif(self.frame_plots.winfo_ismapped()):
				self.frame_calc.place(x=10, y=270)
				self.frame_plots.place_forget()

	def OpenSectionWin(self):
		SectionWindow = SecWin.ShaftSectionWindow(self.root, self.controller)

	def OpenStressWin(self):
		StressWindow = StrWin.ShaftStressWindow(self.root, self.controller)

	def OpenForceWin(self):
		ForceWindow = ForWin.ShaftForceWindow(self.root, self.controller)

	def OpenSupportWin(self):
		SupportWindow = SupWin.ShaftSupportWindow(self.root, self.controller)

	def RemoveSection(self):
		s = self.tree_sections.focus()
		self.controller.RemoveSection(self.tree_sections.index(s))

	def RemoveStress(self):
		s = self.tree_stress.focus()
		self.controller.RemoveStress(self.tree_stress.index(s))

	def RemoveForce(self):
		f = self.tree_forces.focus()
		self.controller.RemoveForce(self.tree_forces.index(f))

	def DrawPlot(self, event):
		for i in self.listbox_plots.curselection():
			self.controller.PlotInCanvas(self.listbox_plots.get(i))
			print(self.listbox_plots.get(i))

	def DrawOrientationCanvas(self):
		self.canvas_axial.create_line(((10,240),(10,220)), fill='black', width=1)
		self.canvas_axial.create_line(((10,240),(30,240)), fill='black', width=1)
		self.canvas_axial.create_polygon(((5,220),(10,210),(15,220)),fill='black')
		self.canvas_axial.create_polygon(((30,235),(40,240),(30,245)),fill='black')
		self.canvas_axial.create_text((45, 240), text='z', fill='black', font='tkDefaultFont 10')
		self.canvas_axial.create_text((10, 200), text='y', fill='black', font='tkDefaultFont 10')
		self.canvas_long.create_line(((10,240),(10,220)), fill='black', width=1)
		self.canvas_long.create_line(((10,240),(30,240)), fill='black', width=1)
		self.canvas_long.create_polygon(((5,220),(10,210),(15,220)),fill='black')
		self.canvas_long.create_polygon(((30,235),(40,240),(30,245)),fill='black')
		self.canvas_long.create_text((45, 240), text='x', fill='black', font='tkDefaultFont 10')
		self.canvas_long.create_text((10, 200), text='y', fill='black', font='tkDefaultFont 10')

	def run(self):
		self.root.mainloop()
#}}}
