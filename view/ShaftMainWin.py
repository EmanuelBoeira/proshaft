#main window for shaft project

import tkinter as tk
import tkinter.ttk as ttk

class ShaftMainWindow:
	def __init__(self):
		#tk instance
		self.root = tk.Tk()

		#window atributes
		self.root.geometry('700x700')
		self.root.title('proshaft')
		self.root.resizable(False, False)

		#root elements
		canvas_axial = tk.Canvas(self.root, width=250, height=250, bg='white')
		canvas_axial.place(x=10, y=10)

		canvas_long = tk.Canvas(self.root, width=420, height=250, bg='white')
		canvas_long.place(x=270, y=10)

		frame_draw = ttk.Frame(self.root, width=680, height=400)
		frame_draw.place(x=10, y=270)

		tree_sections = ttk.Treeview(frame_draw)
		tree_sections.place(x=0, y=0, width=335, height=260)
		treeviewScroll1 = tk.Scrollbar(tree_sections, orient=tk.VERTICAL)
		treeviewScroll1.pack(side=tk.RIGHT, fill=tk.Y)


	def run(self):
		self.root.mainloop()

#test
win = ShaftMainWindow()
win.run()
