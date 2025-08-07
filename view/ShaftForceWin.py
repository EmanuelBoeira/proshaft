#window for add a force in the shaft project
#v1.0 concluido!!!
import tkinter as tk
import tkinter.ttk as ttk

class ShaftForceWindow: 
	def __init__(self, origin, controller):
		#instancia de tk.
		self.root = tk.Toplevel(origin)
		self.controller = controller

		self.plane_xy = tk.BooleanVar()
		self.tangential = tk.BooleanVar()

		#atributos da janela.
		self.root.title('Adicionar força')
		self.root.geometry('500x300')
		self.root.resizable(False, False)

		#elementos de root.
		self.text1 = tk.Label(self.root, text='Plano:')
		self.text1.place(x=30, y=50)

		self.xy = ttk.Radiobutton(self.root, text='xy', value=True, variable=self.plane_xy)
		self.xy.place(x=50, y=70)

		self.xz = ttk.Radiobutton(self.root, text='xz', value=False, variable=self.plane_xy)
		self.xz.place(x=50, y=90)

		self.text2 = ttk.Label(self.root, text='Direção:')
		self.text2.place(x=30, y=130)

		self.t = ttk.Radiobutton(self.root, text='tangencial', variable=self.tangential, value=True)
		self.t.place(x=50, y=150)

		self.r = ttk.Radiobutton(self.root, text='radial', variable=self.tangential, value=False)
		self.r.place(x=50, y=170)

		self.text3 = tk.Label(self.root, text='F(N):')
		self.text3.place(x=250, y=50)

		self.F = tk.Entry(self.root, width=100)
		self.F.place(x=360, y=50, width=100)

		self.text4 = tk.Label(self.root, text='x(mm):')
		self.text4.place(x=250, y=90)

		self.x = tk.Entry(self.root, width=100)
		self.x.place(x=360, y=90, width=100)

		self.text5 = tk.Label(self.root, text='y ou z(mm):')
		self.text5.place(x=250, y=130)

		self.yorz = tk.Entry(self.root, width=100)
		self.yorz.place(x=360, y=130, width=100)

		self.buttonAdd = tk.Button(self.root, text='Adicionar', command = lambda: [self.AddForce(), self.controller.UpdateForceTreeview(), self.controller.UpdateCanvas(), self.root.destroy()])
		self.buttonAdd.place(x=220, y=240, width=120, height=30)

		self.buttonCancel = tk.Button(self.root, text='Cancelar', command = self.root.destroy)
		self.buttonCancel.place(x=360, y=240, width=120, height=30)

	def AddForce(self):
		self.controller.AddForceToModel(float(self.x.get()), float(self.yorz.get()), self.tangential.get(), self.plane_xy.get(), float(self.F.get()))
