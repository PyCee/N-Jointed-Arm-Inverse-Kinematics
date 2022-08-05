import tkinter
from tkinter.font import Font
from vector import Vector

DEFAULT_LENGTH = 1.0
DEFAULT_LOWER_LIMIT = -3.14159 / 2
DEFAULT_UPPER_LIMIT = 3.14159 / 2
DEFAULT_WEIGHT = 0.7

class InvalidParameterException(Exception):
    pass
class Parameters_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)

        self.__N = 0
        
        self.update_parameters_callback = lambda : None
        self.length_title_label = None
        self.lower_limits_title_label = None
        self.upper_limits_title_label = None
        self.weight_title_label = None
        
        self.length_labels = []
        self.length_boxes = []
        self.remove_buttons = []

        self.limits_labels = []
        self.lower_limits_boxes = []
        self.upper_limits_boxes = []

        self.weight_labels = []
        self.weight_boxes = []
        
        append_button = tkinter.Button(self, text="Add New Joint",
                                       command=self.append_joint)
        append_button.place(x=10, y=10)

        self.length_vcmd = (self.register(self.validate_length),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.limit_vcmd = (self.register(self.validate_limit),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.weight_vcmd = (self.register(self.validate_weight),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
    def get_N(self):
        return self.__N
    def bind_update_parameters_event(self, update_parameters_event):
        self.update_parameters_callback = update_parameters_event

    def append_joint(self):
        self.append_length()
        self.append_limits()
        if self.get_N() >= 2:
            self.append_weight()    
        self.__N += 1
        self.update_parameters()
        
    def append_length(self):
        if self.length_title_label == None:
            self.length_title_label = tkinter.Label(self,
                                               text="Lengths")
            self.length_title_label.place(x=50, y=50)
            f = Font(self.length_title_label,
                     self.length_title_label.cget("font"))
            f.configure(underline = True)
            self.length_title_label.configure(font=f)
            
        
        y_val = 75 + self.get_N() * 20
        l_label = tkinter.Label(self,
                              text="L" + str(self.get_N()+1) + ":")
        l_label.place(x=20, y=y_val)
        l_box = tkinter.Entry(self, width=10, justify="center",
                            validate='key',
                            validatecommand=self.length_vcmd)
        l_box.place(x=50, y=y_val)
        l_box.insert(0, str(DEFAULT_LENGTH))
        l_box.bind("<FocusOut>", self.update_parameters)
        l_box.bind("<Return>", self.update_parameters)
        
        remove_event = lambda self=self: self.remove_length(self.get_N())
        remove_button = tkinter.Button(self, fg="#ff0000",
                                       text="X", padx=0, pady=0,
                                       command=remove_event)
        remove_button.place(x=140, y=y_val)
        
        self.length_labels.append(l_label)
        self.length_boxes.append(l_box)
        self.remove_buttons.append(remove_button)
        
    def append_limits(self):
        if self.lower_limits_title_label == None:
            self.lower_limits_title_label = tkinter.Label(self,
                                               text="Lower Limits")
            self.lower_limits_title_label.place(x=220, y=50)
            f = Font(self.lower_limits_title_label,
                     self.lower_limits_title_label.cget("font"))
            f.configure(underline = True)
            self.lower_limits_title_label.configure(font=f)
            self.upper_limits_title_label = tkinter.Label(self,
                                               text="Upper Limits")
            self.upper_limits_title_label.place(x=320, y=50)
            f = Font(self.upper_limits_title_label,
                     self.upper_limits_title_label.cget("font"))
            f.configure(underline = True)
            self.upper_limits_title_label.configure(font=f)
            
        y_val = 75 + self.get_N() * 20
        label = tkinter.Label(self, text="Lim"+str(self.get_N())+":")
        label.place(x=175, y=y_val)
        self.limits_labels.append(label)
        
        lower_lim_box = tkinter.Entry(self, width=10,
                            justify="center",
                            validate='key',
                            validatecommand=self.limit_vcmd)
        lower_lim_box.place(x=220, y=y_val)
        lower_lim_box.insert(0, str(DEFAULT_LOWER_LIMIT))
        lower_lim_box.bind("<FocusOut>", self.update_parameters)
        lower_lim_box.bind("<Return>", self.update_parameters)
        self.lower_limits_boxes.append(lower_lim_box)
        
        upper_lim_box = tkinter.Entry(self, width=10,
                            justify="center",
                            validate='key',
                            validatecommand=self.limit_vcmd)
        upper_lim_box.place(x=320, y=y_val)
        upper_lim_box.insert(0, str(DEFAULT_UPPER_LIMIT))
        upper_lim_box.bind("<FocusOut>", self.update_parameters)
        upper_lim_box.bind("<Return>", self.update_parameters)
        self.upper_limits_boxes.append(upper_lim_box)
        
    def append_weight(self):
        index = self.get_N() - 2
        if self.weight_title_label == None:
            self.weight_title_label = tkinter.Label(self,
                                               text="Weights")
            self.weight_title_label.place(x=470, y=50)
            f = Font(self.weight_title_label,
                     self.weight_title_label.cget("font"))
            f.configure(underline = True)
            self.weight_title_label.configure(font=f)
            
        weight_y_val = 75 + (index) * 20
        w_label = tkinter.Label(self,
                                text="W"+str(index)+":")
        w_label.place(x=440, y=weight_y_val)
        w_box = tkinter.Entry(self, width=10,
                              justify="center",
                              validate='key',
                              validatecommand=self.weight_vcmd)
        w_box.place(x=470, y=weight_y_val)
        w_box.insert(0, str(DEFAULT_WEIGHT))
        w_box.bind("<FocusOut>", self.update_parameters)
        w_box.bind("<Return>", self.update_parameters)
        self.weight_labels.append(w_label)
        self.weight_boxes.append(w_box)

    def remove_weight(self):
        self.weight_labels[-1].destroy()
        self.weight_labels = self.weight_labels[:-1]
        self.weight_boxes[-1].destroy()
        self.weight_boxes = self.weight_boxes[:-1]
            
    def remove_length(self, index):

        def replace_with_next(li, index):
            next_value = li[i+1].get()
            li[i].delete(0, tkinter.END)
            li[i].insert(0, str(next_value))
            
        for i in range(index, self.get_N()-1):
            replace_with_next(self.length_boxes, i)
            replace_with_next(self.lower_limits_boxes, i)
            replace_with_next(self.upper_limits_boxes, i)
            
        self.length_labels[-1].destroy()
        self.length_labels = self.length_labels[:-1]
        self.length_boxes[-1].destroy()
        self.length_boxes = self.length_boxes[:-1]
        self.remove_buttons[-1].destroy()
        self.remove_buttons = self.remove_buttons[:-1]
        
        self.limits_labels[-1].destroy()
        self.limits_labels = self.limits_labels[:-1]
        self.lower_limits_boxes[-1].destroy()
        self.lower_limits_boxes = self.lower_limits_boxes[:-1]
        self.upper_limits_boxes[-1].destroy()
        self.upper_limits_boxes = self.upper_limits_boxes[:-1]
        
        if self.get_N() > 2:
            self.remove_weight()

        self.__N -= 1
        
        self.update_parameters()

    def get_lengths(self):
        return [float(box.get()) for box in self.length_boxes]
    def get_lower_limits(self):
        return [float(box.get()) for box in self.lower_limits_boxes]
    def get_upper_limits(self):
        return [float(box.get()) for box in self.upper_limits_boxes]
    def get_weights(self):
        return [float(box.get()) for box in self.weight_boxes]
            
    def update_parameters(self, *args):
        if(self.get_N() >= 2):
            self.update_parameters_callback()
        
    def validate_length(self, action, index, value, prior_value,
                        text, validation_type, trigger_type,
                        widget_name):
        result = True
        if action == '1':
            for c in text:
                if c not in '0123456789.':
                    result = False
            try:
                if value != ".":
                    float(value)
            except ValueError:
                result = False
        return result
    def validate_limit(self, action, index, value, prior_value,
                       text, validation_type, trigger_type,
                       widget_name):
        result = True
        if action == '1':
            for c in text:
                if c not in '-0123456789.':
                    result = False
        return result
    def validate_weight(self, action, index, value, prior_value,
                        text, validation_type, trigger_type,
                        widget_name):
        result = True
        if action == '1':
            for c in text:
                if c not in '0123456789.':
                    result = False
            try:
                if value != ".":
                    f = float(value)
                    if f < 0.0 or f > 1.0:
                        result = False
            except ValueError:
                result = False
        return result
