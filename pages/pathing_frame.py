import tkinter
from tkinter import ttk
from n_jointed_arm_ik import Vector
from path_controller import Path_Instant, Path_Controller

class Pathing_Frame_Alter(tkinter.Toplevel):
    def __init__(self, frame, item, old_t, old_x, old_y):
        self.page_frame = frame
        self.item = item
        super().__init__(frame)
        self.wm_title("Alter Row")
        self.geometry("320x110+0+0")
        
        t_label = tkinter.Label(self, text="T")
        t_label.place(x=57, y=10)
        x_label = tkinter.Label(self, text="X")
        x_label.place(x=157, y=10)
        y_label = tkinter.Label(self, text="Y")
        y_label.place(x=257, y=10)

        self.t_entry = tkinter.Entry(self, width=10, justify="center")
        self.t_entry.insert(0, old_t)
        self.t_entry.place(x=20, y=30)
        self.x_entry = tkinter.Entry(self, width=10, justify="center")
        self.x_entry.insert(0, old_x)
        self.x_entry.place(x=120, y=30)
        self.y_entry = tkinter.Entry(self, width=10, justify="center")
        self.y_entry.insert(0, old_y)
        self.y_entry.place(x=220, y=30)
        
        set_row_button = tkinter.Button(self, text="Update Row",
                                        command=self.set_row)
        set_row_button.place(x=100, y=70)
        
    def set_row(self):
        values = (float(self.t_entry.get()),
                  float(self.x_entry.get()),
                  float(self.y_entry.get()))
        self.page_frame.set_tree_row(self.item, values)
        self.destroy()
        
class Pathing_Frame(tkinter.Frame):
    def __init__(self, root, update_point_event):
        super().__init__(root, width=1000, height=1000)
        
        self.path_controller = None
        self.timing_job = None
        self.update_point_event = update_point_event
        
        self.row_count = 5

        self.tree = ttk.Treeview(self, columns=("T", "X", "Y"),
                                 show="headings", height=self.row_count)
        self.tree.bind("<Double-1>", self.on_row_select)
        self.tree.place(x=20, y=20)
        self.tree.column("T", width=60, anchor='e')
        self.tree.column("X", width=120, anchor='e')
        self.tree.column("Y", width=120, anchor='e')
        self.tree.heading("T", text="T")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")

        for i in range(self.row_count):
            self.tree.insert("", 'end',
                             values=(float(i), 0.0, 0.0))
        
        self.set_key_point_button = tkinter.Button(self, text="Start Path")
        self.set_key_point_button.config(command=self.start_path)
        self.set_key_point_button.place(x=20, y=240)

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
        
    def set_tree_row(self, item, new_values):
        self.tree.delete(item)
        added = False
        for i in range(self.row_count - 1):
            curr_item = self.tree.get_children()[i]
            curr_value = self.tree.item(curr_item)['values'][0]
            if new_values[0] < float(curr_value):
                self.tree.insert("", i, values=new_values)
                added = True
                break
        if not added:
            self.tree.insert("", 'end', values=new_values)
        
    def start_path(self):
        self.path_controller = Path_Controller()
        self.path_controller.set_update_point_event(self.update_point_event)

        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            instant = Path_Instant(float(values[0]),
                                   Vector(float(values[1]),
                                          float(values[2])))
            self.path_controller.add_instant(instant)
        
        if self.timing_job != None:
            self.after_cancel(self.timing_job)
        self.timing_job = self.after(10, self.update_path)
        
    def update_path(self):
        self.path_controller.step(0.01)
        if not self.path_controller.is_finished():
            self.timing_job = self.after(10, self.update_path)
        else:
            self.timing_job = None
            
