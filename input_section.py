import tkinter

MAX_INPUT = 10

class Input_Section:
    def __init__(self, parent, title, position, widget):
        self.title = title
        self.position = position
        self.label = tkinter.Label(parent, text=title)
        self.label.place(x=position.x, y=position.y)
        self.widget = widget
        self.set_position(position)
    def set_position(self, position):
        self.label.place(x=position.x, y=position.y)
        self.widget.place(x=position.x + 7*len(self.title),
                          y=position.y)
    def get(self):
        return self.widget.get()
class Input_Box (Input_Section):
    def __init__(self, parent, title, position):
        widget = tkinter.Entry(parent, width=10, justify="center")
        super().__init__(parent, title, position, widget)
class Input_Slider (Input_Section):
    def __init__(self, parent, title, position, command_):
        widget = tkinter.Scale(parent, from_=0, to=1,
                               resolution=0.001,
                               orient=tkinter.HORIZONTAL,
                               command=command_)
        super().__init__(parent, title, position, widget)
