import os
import tkinter
from tkinter import END, Checkbutton, PhotoImage, ttk
from turtle import color
from pages.pathing.tree_entry import Tree_Entry
from vector import Vector
from pages.pathing.path import Path
from pages.pathing.piecewise_function import Piecewise_Function
import display_settings

COL_START_T = '#1'
COL_END_T = '#2'
COL_X = '#3'
COL_Y = '#4'
COL_END_POINT = '#5'

COL_WIDTHS = {COL_START_T: 75,
                COL_END_T: 75,
                COL_X: 150,
                COL_Y: 150,
                COL_END_POINT: 75}
EDITABLE_COL = [COL_START_T, COL_END_T, COL_X, COL_Y]

class Pathing_Frame(tkinter.Frame):
    def __init__(self, root, update_point_event):
        super().__init__(root, width=1000, height=1000)

        self.path = None
        self.timing_job = None
        self.update_point_event = update_point_event
        self.current_tree_entry = None

        self.tree = ttk.Treeview(self, columns=("start_t", "end_t", "X", "Y", "end_point"),
                                 show="headings", height=0)
        self.tree.bind("<Double-1>", self.on_row_select)
        self.tree.place(x=55, y=45)
        self.tree.column("start_t", width=COL_WIDTHS[COL_START_T], anchor='c')
        self.tree.column("end_t", width=COL_WIDTHS[COL_END_T], anchor='c')
        self.tree.column("X", width=COL_WIDTHS[COL_X], anchor='c')
        self.tree.column("Y", width=COL_WIDTHS[COL_Y], anchor='c')
        self.tree.column("end_point", width=COL_WIDTHS[COL_END_POINT], anchor='c')
        self.tree.heading("start_t", text="Start")
        self.tree.heading("end_t", text="End")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")
        self.tree.heading("end_point", text="End Point")
        
        self.setup_text()

        
        self.add_row_BTN = tkinter.Button(self, text="Add New Row")
        self.add_row_BTN.config(command=self.on_row_append)
        self.update_new_row_button_position()

        self.start_path_BTN = tkinter.Button(self,
                                                   text="Start Path")
        self.start_path_BTN.config(command=self.start_path)
        self.start_path_BTN.place(x=650, y=15)
        
        self.loop_path_CB = Checkbutton(self,
                                         variable=display_settings.LoopPath,
                                         text="Loop Path")
        self.loop_path_CB.place(x=630, y=40)

        self.initialize_default()

    def setup_text(self):
        self.setup_single_text(COL_X, "Ex: 1 + cos(t * 2 * pi) / 2")
        self.setup_single_text(COL_Y, "Ex: sin(t * 2 * pi) / 2")

    def setup_single_text(self, col, text):
        text_label = tkinter.Label(self,
            state="disabled", justify=tkinter.LEFT , text=text)
        
        x = self.get_x_offset_of_col(col) + 5
        y = self.tree.winfo_rooty() - 25
        width = COL_WIDTHS[col] - 10

        text_label.place(in_=self.tree, x=x, y=y, anchor='nw', width=width)

    def get_x_offset_of_col(self, col):
        #TODO: does python iterate over dicts in order?
        x_offset = 0
        for key in COL_WIDTHS:
            if key == col:
                break
            x_offset += COL_WIDTHS[key]
        return x_offset

    def initialize_default(self):
        default_values = (0, 1, "1 + cos(t * 2 * pi) / 2", "sin(t * 2 * pi) / 2")
        iid = self.add_tree_row(default_values)
        self.update_end_t(iid)

    def validate_row(self, iid):
        values = self.tree.set(iid)
        if values["start_t"] >= values["end_t"]:
            #TODO: big red error
            pass
        cur_row = self.get_piecewise_function(iid)
        prev_row = self.get_piecewise_function(self.tree.prev(iid))
        next_row = self.get_piecewise_function(self.tree.next(iid))
        if prev_row.get_end_point() != cur_row.get_start_point():
            #TODO warning
            pass
        if cur_row.get_end_point() != next_row.get_start_point():
            #TODO: warning
            pass

        return Piecewise_Function(values["start_t"], values["end_t"], values["X"], values["Y"])
        
    def on_row_select(self, e):
        iid = self.tree.focus()
        col = self.tree.identify_column(e.x)
        if col not in EDITABLE_COL:
            return
        self.current_tree_entry = Tree_Entry(self, iid, col)
    
    def set_value(self, iid, col, value):
        '''
        Used to set value in the tree. Called directly by Tree_Entry.
        Updates read-only values.
        '''
        self.current_tree_entry = None
        self.tree.set(iid, col, value)
        self.update_end_t(iid)

    def flush_tree_entry(self):
        if self.current_tree_entry != None:
            self.current_tree_entry.entry_focus_out()

    def update_end_t(self, iid):
        func = self.get_piecewise_function(iid)
        end_point = func.get_end_point()
        end_point_str = "(" + str(round(end_point.x, 2)) + ", " + str(round(end_point.y)) + ")"
        self.tree.set(iid, COL_END_POINT, end_point_str)

    def get_piecewise_function(self, iid):
        values = self.tree.set(iid)
        return Piecewise_Function(values["start_t"], values["end_t"], values["X"], values["Y"])

    def on_row_append(self):
        items = self.tree.get_children(None)
        new_start = 0
        if len(items) > 0:
            new_start = self.tree.set(items[len(items) - 1], COL_END_T)

        default_values = (new_start,
                        float(new_start) + 1,
                        "",
                        "")
        self.add_tree_row(default_values)
        
    def add_tree_row(self, new_values):
        
        new_row_index = self.tree.cget('height')
        self.tree.config(height=new_row_index+1)
        iid = self.tree.insert("", 'end', values=new_values)

        pixel = tkinter.PhotoImage(width=1, height=1)
        #TODO: add "remove row"
        play_event = lambda self=self: self.play_piecewise_row(new_row_index)
        play_button = tkinter.Button(self, image=pixel, text=">", fg="#4D4", width=16, height=16, compound="center", padx=0, pady=0, command=play_event)
        play_button.image = pixel
        
        test = self.tree.item(iid)
        play_button.place(in_=self.tree, x=-30, y=25 + 20 * new_row_index)
        self.update_new_row_button_position()
        return iid
    def update_new_row_button_position(self):
        x = 200
        num_rows = self.tree.cget('height')
        y = 40 + 20 * num_rows
        self.add_row_BTN.place(in_=self.tree, x=x, y=y)

    def get_iid_from_index(self, index):
        return self.tree.get_children(None)[index]

    def play_piecewise_row(self, index):
        self.start_path([self.get_iid_from_index(index)])

    def start_path(self, function_indexes=None):
        self.flush_tree_entry()
        path_functions = self.get_path_functions(function_indexes)
        self.path = Path(path_functions)
        self.__dt = self.path.get_start()
        
        if self.timing_job != None:
            self.after_cancel(self.timing_job)
        self.timing_job = self.after(10, self.update_path)

    def get_path_functions(self, function_indexes = None):
        functions = []
        if function_indexes == None:
            function_indexes = self.tree.get_children(None)
        for iid in function_indexes:
            functions.append(self.get_piecewise_function(iid))
        return functions

    def update_path(self):
        duration = self.path.get_duration()
        if self.__dt > duration:
            if display_settings.LoopPath.get():
                self.__dt = 0
            else:
                self.__dt = duration
        if self.__dt < duration:
            self.timing_job = self.after(10, self.update_path)
        
        point = self.path.get_point(self.__dt)
        self.update_point_event(point)
        self.__dt += 0.01