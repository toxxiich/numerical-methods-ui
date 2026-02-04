from tkinter import *
import webbrowser
from tkinter import font
from turtledemo.penrose import makeshapes
import matplotlib.pyplot as plt
import numpy as np


class MainApp:
	def __init__(self):
		self.root = Tk()
		self.window = MainWindow(self.root)
		self.root.geometry('400x400')
	def run(self):
		self.root.mainloop()
	def exit_app(self):
		self.root.destroy()

class MainWindow:
	def __init__(self, root):
		self.root = root
		self.makeMenu()
		self.make_copyrignt()
		self.content_frame = Frame(self.root)
		self.content_frame.pack(expand=True, fill=BOTH)
		self.current_frame = None
		self.switch_to_frame(WelcomeFrame)

	def makeMenu(self):
		self.menu = Menu(self.root)
		self.root.config(menu=self.menu)
		self.method_menu = Menu(self.menu, tearoff=0)
		self.method_menu.add_command(label='Интегралы',
		                             command=self.open_integrals,
		                             underline=0)
		self.method_menu.add_command(label='Нелинейные уравнения',
		                             command=self.open_rootfind,
		                             underline=0)
		self.method_menu.add_command(label='Аппроксимация',
		                             command=self.open_approx,
		                             underline=0)
		self.method_menu.add_command(label='Интерполяция',
		                             command=self.open_interpolation,
		                             underline=0)
		self.method_menu.add_command(label='Дифуры',
		                             command=self.open_diff_eql,
		                             underline=0)
		self.menu.add_cascade(label='Вычислить',
		                      menu=self.method_menu,
		                      underline=0)
		self.menu.add_command(label='About', command=self.open_about)

	def make_copyrignt(self):
		self.footerFrame = Frame(self.root)
		self.footerFrame.pack(side=BOTTOM, fill=X)
		self.copyright_text = Label(self.footerFrame,
		                            font=('Tahoma', 8),
		                            text='© 2026 СПбГАСУ'
		                            )
		self.github_label = Label(self.footerFrame,
		                          text='GitHub',
		                          font=("Tahoma", 8, "underline"),
		                          cursor='hand2')
		self.github_label.pack(side=RIGHT, padx=(0, 5))
		self.copyright_text.pack(anchor=SE, padx=(0, 15))
		self.github_label.bind('<Button-1>', self.open_github)
		self.github_label.bind('<Enter>',
		                       lambda e: self.github_label.config(fg='purple'))
		self.github_label.bind('<Leave>',
		                       lambda e: self.github_label.config(fg='black'))

	def switch_to_frame(self, frame_class):
		if self.current_frame is not None:
			self.current_frame.destroy()
		self.current_frame = frame_class(self.content_frame)
		self.current_frame.pack(expand=True, fill=BOTH)

	def open_about(self):
		AboutWindow(self.root)

	def open_github(self, event):
		webbrowser.open('https://github.com/toxxiich')

	def open_integrals(self):
		self.switch_to_frame(IntegralFrame)
	def open_rootfind(self):
		self.switch_to_frame(RootFindingFrame)
	def open_approx(self):
		self.switch_to_frame(ApproximationFrame)
	def open_interpolation(self):
		self.switch_to_frame(InterpolationFrame)
	def open_diff_eql(self):
		self.switch_to_frame(DifferentialEquationFrame)

class AboutWindow:
	def __init__(self, parent):
		self.about_window = Toplevel(parent)
		self.about_window.title('О курсовом проекте')
		self.about_window.geometry('300x300')
		self.center_window(300, 300)

		self.project_text = Label(self.about_window,
		             text='[ Computational Mathematics Suite ]\n'
		                  'Version:       1.0.0 (Release)\n'
		                  'Build date:    February 2026\n'
		                  'Developer:     Sushitski A.O.\n'
		                  'University:    SPbGASU\n'
		                  'Faculty:       Applied Mathematics\n'
		                  'Group:         3PMIb-1\n\n'
		                  '────────────────────\n'
		                  'IMPLEMENTED METHODS:\n'
		                  '• Numerical Integration\n'
		                  '• Dichotomy Method\n'
		                  '• Least Squares (LSM)\n'
		                  '• Multiple Regression (MCM)\n'

		                  'This software is developed as part\n'
		                  'of the computational mathematics\n'
		                  'course project.\n',
		             justify=CENTER,
		             font=('Consolas', 9)
		             )
		self.project_text.pack()

	def center_window(self, width, height):
		self.about_window.update_idletasks()
		parent = self.about_window.master
		parent_x = parent.winfo_x()
		parent_y = parent.winfo_y()
		parent_w = parent.winfo_width()
		parent_h = parent.winfo_height()
		self.about_window.transient(parent)
		self.about_window.grab_set()

		x = parent_x + (parent_w - width) // 2
		y = parent_y + (parent_h - height) // 2

		self.about_window.geometry(f"{width}x{height}+{x}+{y}")


class WelcomeFrame(Frame):
	def __init__(self, main_frame):
		Frame.__init__(self, main_frame)
		self.make_welcome_text()
		self.pack(expand=True, fill=BOTH)
	def make_welcome_text(self):
		self.welcome_text = Label(self,
		             text='Добро пожаловать!\n\n'
		                  'Выберите метод вычисления в меню выше:\n'
		                  '• Вычисление интегралов\n'
		                  '• Метод дихотометрии\n'
		                  '• Метод наименьших квадратов (МНК)\n'
		                  '• Метод кратных регрессий (МКР)',
		             font=('Arial', 10),
		             justify=CENTER,
		             padx=20,
		             pady=20)
		self.welcome_text.pack(expand=True, fill=BOTH)

class IntegralFrame(Frame):
	def __init__(self, main_frame):
		Frame.__init__(self, main_frame)
		self.make_widgets()
	def make_widgets(self):
		self.test_text = Label(self, text='Сегодня хорошая погода')
		self.test_text.pack(expand=True, fill=BOTH)

class RootFindingFrame(Frame):
	def __init__(self, main_frame):
		Frame.__init__(self, main_frame)
		self.make_widgets()
	def make_widgets(self):
		self.test_text = Label(self, text="Here'll be some Nonlinear "
		                                  "Equations stuff")
		self.test_text.pack(expand=True, fill=BOTH)

class ApproximationFrame(Frame):
	def __init__(self, main_frame):
		Frame.__init__(self, main_frame)
		self.make_widgets()
	def make_widgets(self):
		self.test_text = Label(self, text="Here'll be some approximation "
		                                  "stuff")
		self.test_text.pack(expand=True, fill=BOTH)

class InterpolationFrame(Frame):
	def __init__(self, main_frame):
		Frame.__init__(self, main_frame)
		self.make_widgets()
	def make_widgets(self):
		self.test_text = Label(self, text="Here'll be some Interpolation "
		                                  "stuff")
		self.test_text.pack(expand=True, fill=BOTH)

class DifferentialEquationFrame(Frame):
	def __init__(self, main_frame):
		Frame.__init__(self, main_frame)
		self.make_widgets()

	def make_widgets(self):
		self.test_text = Label(self, text="Here'll be some "
		                                  "sifferential equations stuff")
		self.test_text.pack(expand=True, fill=BOTH)

if __name__ == "__main__":
    app = MainApp()
    app.run()