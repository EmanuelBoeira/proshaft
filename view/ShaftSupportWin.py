#window for add a support to the shaft project.
#v1.0 concluida
import tkinter as tk
import tkinter.ttk as ttk

class ShaftSupportWindow:
	def __init__(self, origin, controller):
		#instancia de tk.
		self.root = tk.Toplevel(origin)
		self.controller = controller

		#atributos da janela.
		self.root.title('Adicionar suporte')
		self.root.geometry('300x200')
		self.root.resizable(False, False)

		#elementos de root.
		self.support = tk.StringVar()
		frame_sup = ttk.Labelframe(self.root, text='Suporte:', width=280, height=70)
		frame_sup.place(x=10, y=5)

		r1 = ttk.Radiobutton(frame_sup, text='1', value='0', variable=self.support)
		r1.place(x=70, y=10)

		r2 = ttk.Radiobutton(frame_sup, text='2', value='1', variable=self.support)
		r2.place(x=150, y=10)

		self.text1 = tk.Label(self.root, text='x(mm):')
		self.text1.place(x=55, y=100)

		self.x = tk.Entry(self.root, width=100)
		self.x.place(x=145, y=100, width=100)

		self.buttonAddSupp = ttk.Button(self.root, text='Modificar', command = lambda: [self.controller.ModifySupport(float(self.x.get()), int(self.support.get())), self.controller.UpdateCanvas(), self.root.destroy()])
		self.buttonAddSupp.place(x=160, y=160, width=120, height=30)

		self.buttonCancel = tk.Button(self.root, text='Cancelar', command = self.root.destroy)
		self.buttonCancel.place(x=20, y=160, width=120, height=30)
