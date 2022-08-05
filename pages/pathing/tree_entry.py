import tkinter

class Tree_Entry(tkinter.Entry):
	def __init__(self, pathing_frame, iid, col):
		self.__pathing_frame = pathing_frame
		self.__tree = pathing_frame.tree
		super().__init__(self.__tree)
		self.__iid = iid
		self.__col = col
		val = self.__tree.set(iid, col)
		x, y, w, h = self.__tree.bbox(iid, col)

		self.insert(tkinter.END, val)
		self.place(x=x + self.winfo_x(),
					y=y + self.winfo_y(),
					width=w, height=h)
		self.focus_set()
		self.select_range(0, 'end')
		self.icursor('end')
		self.start_bindings()

	def check_click_target(self, e):
		if(e.widget != self):
			self.entry_focus_out()

	def entry_focus_out(self):
		value = self.get()
		self.__pathing_frame.set_value(self.__iid, self.__col, value)
		self.stop_bindings()
		self.destroy()

	def start_bindings(self):

		on_focus_out = lambda e : self.entry_focus_out()
		self.bind("<FocusOut>", on_focus_out)
		self.bind("<Return>", on_focus_out)
		
		on_click = lambda e : self.check_click_target(e)
		self.__pathing_frame.bind("<Button-1>", on_click)

	def stop_bindings(self):
		self.unbind("<FocusOut>")
		self.unbind("<Return>")
		self.__pathing_frame.unbind("<Button-1>")