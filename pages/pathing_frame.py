import tkinter
from tkinter import ttk
from n_jointed_arm_ik import Vector
from path_controller import Piecewise_Function, Path_Controller


class Pathing_Frame_Alter(tkinter.Toplevel):
    def __init__(self, frame, item, old_t, old_x, old_y):
        self.page_frame = frame
        self.item = item
        super().__init__(frame)
        self.wm_title("Alter Row")
        self.geometry("320x120+0+0")
        
        t_label = tkinter.Label(self, text="t-range")
        t_label.place(x=20, y=10)
        x_label = tkinter.Label(self, text="x function")
        x_label.place(x=20, y=34)
        y_label = tkinter.Label(self, text="y function")
        y_label.place(x=20, y=58)

        self.t_entry = tkinter.Entry(self, width=24, justify="center")
        self.t_entry.insert(0, old_t)
        self.t_entry.place(x=100, y=10)
        self.x_entry = tkinter.Entry(self, width=24, justify="center")
        self.x_entry.insert(0, old_x)
        self.x_entry.place(x=100, y=34)
        self.y_entry = tkinter.Entry(self, width=24, justify="center")
        self.y_entry.insert(0, old_y)
        self.y_entry.place(x=100, y=58)
        
        set_row_button = tkinter.Button(self, text="Update Row",
                                        command=self.set_row)
        set_row_button.place(x=100, y=82)
        
    def set_row(self):
        values = (str(self.t_entry.get()),
                  str(self.x_entry.get()),
                  str(self.y_entry.get()))
        self.page_frame.set_tree_row(self.item, values)
        self.destroy()

class Pathing_Frame(tkinter.Frame):
    def __init__(self, root, update_point_event):
        super().__init__(root, width=1000, height=1000)

        self.path_controller = None
        self.timing_job = None
        self.update_point_event = update_point_event
        

        self.tree = ttk.Treeview(self, columns=("T", "X", "Y"),
                                 show="headings", height=0)
        self.tree.bind("<Double-1>", self.on_row_select)
        self.tree.place(x=5, y=5)
        self.tree.column("T", width=180, anchor='c')
        self.tree.column("X", width=180, anchor='c')
        self.tree.column("Y", width=180, anchor='c')
        self.tree.heading("T", text="T")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")
        
        self.set_key_point_button = tkinter.Button(self,
                                                   text="Start Path")
        self.set_key_point_button.config(command=self.start_path)
        self.set_key_point_button.place(x=20, y=240)
        
        self.add_row_b = tkinter.Button(self, text="Add New Row")
        self.add_row_b.config(command=self.on_row_append)
        self.add_row_b.place(x=20, y=270)

        self.label_frame = tkinter.LabelFrame(self, padx=10, pady=10)
        self.label_frame.place(x=20, y=300)
        self.description="Create paths for the point to follow. ANIMATION!"
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=200)
        self.label_text.pack()
        
    def on_row_select(self, e):
        item = self.tree.selection()[0]
        old_t, old_x, old_y = self.tree.item(item, "values")
        alter_win = Pathing_Frame_Alter(self, item, old_t, old_x, old_y)
    def on_row_append(self):
        alter_win = Pathing_Frame_Alter(self, None, "", "", "")
        
    def set_tree_row(self, item, new_values):
        if item != None:
            self.tree.delete(item)
        else:
            prev_height = self.tree.cget('height')
            self.tree.config(height=prev_height+1)
        self.tree.insert("", 'end', values=new_values)
        
    def start_path(self):
        self.path_controller = Path_Controller()
        self.path_controller.set_update_point_event(self.update_point_event)
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            func = Piecewise_Function(str(values[0]),
                                      str(values[1]),
                                      str(values[2]))
            self.path_controller.add_piecewise_function(func)
        
        if self.timing_job != None:
            self.after_cancel(self.timing_job)
        self.timing_job = self.after(10, self.update_path)
        
    def update_path(self):
        self.path_controller.step(0.01)
        if not self.path_controller.is_finished():
            self.timing_job = self.after(10, self.update_path)
        else:
            self.timing_job = None
