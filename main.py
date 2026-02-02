from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

def notdone():
	pass

def show_info():
	pass


root = Tk()
top = Menu(root)
root.config(menu=top)
func = Menu(top, tearoff=0)
func.add_command(label='Ингегралы', command=notdone, underline=0)
func.add_command(label='Дихотометрия', command=notdone, underline=0)
func.add_command(label='МНК', command=notdone, underline=0)
func.add_command(label='МКР', command=notdone, underline=0)
top.add_cascade(label='Выберете что хотите', menu=func, underline=0)

about_cascade = Menu(top, tearoff=0)
top.add_command(label='About', command=show_info)



mainloop()