import tkinter

UNITS_RADIANS = 0
UNITS_DEGREES = 1

AngleUnits = tkinter.IntVar()
AngleUnits.set(UNITS_RADIANS)
ShowGrid = tkinter.IntVar()
ShowGrid.set(1)
ShowGridNumbers = tkinter.IntVar()
ShowGridNumbers.set(1)
ShowArmBounds = tkinter.IntVar()
ShowArmBounds.set(1)
ShowAngleText = tkinter.IntVar()
ShowAngleText.set(0)
ShowAngleArc = tkinter.IntVar()
ShowAngleArc.set(0)
ShowLengthText = tkinter.IntVar()
ShowLengthText.set(0)
ShowEndPointCoords = tkinter.IntVar()
ShowEndPointCoords.set(0)
LoopPath = tkinter.IntVar()
LoopPath.set(0)
