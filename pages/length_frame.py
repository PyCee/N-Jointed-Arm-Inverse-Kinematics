import tkinter
from vector import Vector

DEFAULT_LENGTH = 1.0
DEFAULT_WEIGHT = 0.7

class InvalidLengthException(Exception):
    pass
class Length_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)

        self.update_lengths_callback = lambda : None
        self.length_labels = []
        self.length_boxes = []
        self.remove_buttons = []

        self.weight_labels = []
        self.weight_boxes = []
        
        append_button = tkinter.Button(self, text="Add New Length",
                                       command=self.append_length)
        append_button.place(x=10, y=10)

        self.length_vcmd = (self.register(self.validate_length),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.weight_vcmd = (self.register(self.validate_weight),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
    def get_N(self):
        return len(self.length_boxes)
    def bind_update_lengths_event(self, update_lengths_event):
        self.update_lengths_callback = update_lengths_event
    def append_length(self):
        index = self.get_N()
        y_val = 10 + index * 20
        
        l_label = tkinter.Label(self,
                              text="Length "+str(index+1)+":")
        l_label.place(x=160, y=y_val)
        
        l_box = tkinter.Entry(self, width=10, justify="center",
                            validate='key',
                            validatecommand=self.length_vcmd)
        l_box.place(x=240, y=y_val)
        l_box.insert(0, str(DEFAULT_LENGTH))
        l_box.bind("<FocusOut>", self.update_lengths)
        l_box.bind("<Return>", self.update_lengths)
        
        remove_event = lambda self=self: self.remove_length(index)
        remove_button = tkinter.Button(self, fg="#ff0000",
                                       text="X", padx=0, pady=0,
                                       command=remove_event)
        remove_button.place(x=330, y=y_val)
        
        self.length_labels.append(l_label)
        self.length_boxes.append(l_box)
        self.remove_buttons.append(remove_button)

        if index >= 2:
            weight_y_val = 10 + (index-2) * 20
            w_label = tkinter.Label(self,
                                    text="Weight "+str(index-1)+":")
            w_label.place(x=380, y=weight_y_val)
            w_box = tkinter.Entry(self, width=10,
                                  justify="center",
                                  validate='key',
                                  validatecommand=self.weight_vcmd)
            w_box.place(x=460, y=weight_y_val)
            w_box.insert(0, str(DEFAULT_WEIGHT))
            w_box.bind("<FocusOut>", self.update_lengths)
            w_box.bind("<Return>", self.update_lengths)
            self.weight_labels.append(w_label)
            self.weight_boxes.append(w_box)
        
        self.update_lengths()
        
    def remove_length(self, index):
        for i in range(index, self.get_N()-1):
            next_length = self.length_boxes[i+1].get()
            self.length_boxes[i].delete(0, tkinter.END)
            self.length_boxes[i].insert(0, str(next_length))
            
        self.length_labels[-1].destroy()
        self.length_labels = self.length_labels[:-1]
        self.length_boxes[-1].destroy()
        self.length_boxes = self.length_boxes[:-1]
        self.remove_buttons[-1].destroy()
        self.remove_buttons = self.remove_buttons[:-1]

        if self.get_N() >= 2:
            self.weight_labels[-1].destroy()
            self.weight_labels = self.weight_labels[:-1]
            self.weight_boxes[-1].destroy()
            self.weight_boxes = self.weight_boxes[:-1]
        

        self.update_lengths()

    def get_lengths(self):
        lengths = []
        for box in self.length_boxes:
            lengths.append(float(box.get()))
        return lengths
    def get_weights(self):
        weights = []
        for box in self.weight_boxes:
            weights.append(float(box.get()))
        return weights
            
    def update_lengths(self, *args):
        if(self.get_N() >= 2):
            self.update_lengths_callback()
        
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
