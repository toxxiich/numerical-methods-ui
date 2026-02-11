from tkinter import *
from tkinter import messagebox
from integrals import DomainError, ZeroDenominatorError, StepError, \
	EvenStepWarning, EmptyInput, NonNumInput
from PIL import Image, ImageTk
import webbrowser
import integrals
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class MainApp:
	def __init__(self):
		self.root = Tk()
		self.window = MainWindow(self.root)
		self.root.geometry('800x500')
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
		self.current_frame = frame_class(self.content_frame, self)
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
	def open_runge(self):
		self.switch_to_frame(RungeRuleFrame)

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
	def __init__(self, main_frame, main_app):
		Frame.__init__(self, main_frame)
		self.make_welcome_text()
		self.pack(expand=True, fill=BOTH)
		self.main_app = main_app
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
	def __init__(self, main_frame, main_app):
		Frame.__init__(self, main_frame)
		self.main_app = main_app
		self.make_widgets()

	def make_widgets(self):
		self.input_area_frame = Frame(self)
		self.graph_area_frame = Frame(self)
		self.pick_integral_frame = Frame(self.input_area_frame)
		self.input_num_frame = Frame(self.input_area_frame)
		self.output_num_frame = Frame(self.input_area_frame)
		self.input_area_frame.pack(side=LEFT, expand=True, fill=BOTH)
		self.graph_area_frame.pack(side=RIGHT, expand=True, fill=BOTH)
		self.pick_integral_frame.pack(side=TOP, expand=True, fill=BOTH)
		self.input_num_frame.pack(side=TOP, expand=True, fill=BOTH)
		self.output_num_frame.pack(side=BOTTOM, expand=True, fill=BOTH)

		self.selected_integral = IntVar()
		self.selected_integral.set(1)

		self.img1 = Image.open('integral_1.png')
		self.img2 = Image.open('integral_2.png')
		self.photo1 = ImageTk.PhotoImage(self.img1)
		self.photo2 = ImageTk.PhotoImage(self.img2)

		Radiobutton(self.pick_integral_frame,
		                       text='1',
		                       variable=self.selected_integral,
		                       value=1).grid(
			row=0, column=0, padx=5, pady=5
		)
		Radiobutton(self.pick_integral_frame,
		                       text='2',
		                       variable=self.selected_integral,
		                       value=2).grid(
			row=1, column=0, padx=5, pady=5
		)

		Label(self.pick_integral_frame,
		      image=self.photo1).grid(row=0, column=1, padx=5, pady=5)
		Label(self.pick_integral_frame,
		      image=self.photo2).grid(row=1, column=1, padx=5, pady=5)

		Label(self.input_num_frame, text='a').grid(row=0, column=0, padx=5, pady=5)
		Label(self.input_num_frame, text='b').grid(row=1, column=0, padx=5, pady=5)
		Label(self.input_num_frame, text='n').grid(row=2, column=0, padx=5, pady=5)

		self.lower = StringVar()
		self.upper = StringVar()
		self.stride = StringVar()

		Entry(self.input_num_frame, textvariable=self.lower).grid(row=0, column=1, padx=5, pady=5)
		Entry(self.input_num_frame, textvariable=self.upper).grid(row=1, column=1, padx=5, pady=5)
		Entry(self.input_num_frame, textvariable=self.stride).grid(row=2, column=1, padx=5, pady=5)

		Button(self.input_num_frame, text='Запустить ракету',
		                  command=self.printer).grid(row=3, column=0, padx=5, pady=5)
		Button(self.input_num_frame, text='Подбор n',
		       command=self.find_min_n).grid(row=3, column=1, padx=5, pady=5)

		self.results = {}
		self.results['left_rectangle'] = StringVar()
		self.results['right_rectangle'] = StringVar()
		self.results['trapezoidal'] = StringVar()
		self.results['simpson_rule'] = StringVar()
		self.results['min_common_step'] = StringVar()
		self.make_output(self.output_num_frame)

		self.fig = plt.figure(figsize=(5, 4), dpi=100)
		self.ax = self.fig.add_subplot(111)
		self.ax.set_title("Пустой график")

		self.canvas = FigureCanvasTkAgg(self.fig,
		                                master=self.graph_area_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(expand=True, fill=BOTH)

	def printer(self):
		try:
			params = self.get_input()
			results = self.calculate_integrals(params)
			self.update_results(results)
			self.update_plot(params)

		except EmptyInput as e:
			messagebox.showerror(
				"Ошибка ввода",
				e
			)

		except NonNumInput as e:
			messagebox.showerror(
				"Ошибка ввода",
				e
			)

		except StepError as e:
			messagebox.showerror(
				"Ошибка шага",
				e
			)

		except DomainError:
			messagebox.showerror(
				"Ошибка области определения",
				"Функция не определена на данном интервале"
			)

		except ZeroDenominatorError:
			messagebox.showerror(
				"Деление на ноль",
				"Знаменатель обращается в ноль"
			)

		except Exception as e:
			messagebox.showerror(
				"Неизвестная ошибка",
				f'Упс...\nВы нашли ошибку, которую я не '
				f'предусмотел!\n\nПожалуйста, напишите о ней на почту нашего '
				f'разработчика antonsu-spb@yandex.ru и мы обязательно учтем '
				f'её в следующем релизе!\n\nP.S. Ошибка, с которой вы '
				f'столкнулись: {e}'
			)

	def find_min_n(self):
		try:
			self.results['min_common_step'].set(integrals.find_common_step(
				*self.get_input()
			))
		except EmptyInput as e:
			messagebox.showerror(
				"Ошибка ввода",
				e
			)

		except StepError as e:
			messagebox.showerror(
				"Ошибка шага",
				e
			)

		except NonNumInput as e:
			messagebox.showerror(
				"Ошибка ввода",
				e
			)

		except DomainError:
			messagebox.showerror(
				"Ошибка области определения",
				"Функция не определена на данном интервале"
			)

		except ZeroDenominatorError:
			messagebox.showerror(
				"Деление на ноль",
				"Знаменатель обращается в ноль"
			)

		except EvenStepWarning as e:
			messagebox.showerror(
				'Нечетное разбиение',
				'Simpson rule requires even n'
			)

		except Exception as e:
			messagebox.showerror(
				"Неизвестная ошибка",
				f'Упс...\nВы нашли ошибку, которую я не '
				f'предусмотел!\n\nПожалуйста, напишите о ней на почту нашего '
				f'разработчика antonsu-spb@yandex.ru и мы обязательно учтем '
				f'её в следующем релизе!\n\nP.S. Ошибка, с которой вы '
				f'столкнулись: {e}'
			)
		Button(self.output_num_frame, text='Проверить nmin',
		       command=self.check_n).grid(
			row=5, column=1, padx=5, pady=5
		)
	def check_n(self):
		self.stride.set(integrals.find_common_step(*self.get_input()))
		self.printer()

	def get_input(self):
		a = self.lower.get()
		b = self.upper.get()
		n = self.stride.get()

		if self.selected_integral.get() == 1:
			func = integrals.function_1
		elif self.selected_integral.get() == 2:
			func = integrals.function_2

		return func, a, b, n

	def calculate_integrals(self, input_data):
		res_dict = {
			'left_rectangle': integrals.left_rectangle(*input_data),
			'right_rectangle': integrals.right_rectangle(*input_data),
			'trapezoidal': integrals.trapezoidal(*input_data),
		}
		try:
			res_dict['simpson_rule'] = integrals.simpson_rule(*input_data)
		except EvenStepWarning:
			res_dict['simpson_rule'] = 'enter even n!!'
			messagebox.showwarning(
				'Нечетное разбиение',
				'Simpson rule requires even n'
			)
		return res_dict


	def update_results(self, results: dict):
		for key in results:
			self.results[key].set(results[key])

	def update_plot(self, params):
		a, b, n = integrals.validate_input(*params[1:])
		func = params[0]
		MIN_PLOT_POINTS = 500
		n = int(n)

		self.ax.clear()
		x = np.linspace(a, b, max(MIN_PLOT_POINTS, n))
		y = func(x)

		self.ax.plot(x, y)
		self.canvas.draw()

	def make_output(self, parent):
		Label(parent, text='Правые прямоугольников').grid(
			row=0, column=0, padx=5, pady=5
		)
		Label(parent, text='Левые прямоугольники').grid(
			row=1, column=0, padx=5, pady=5,
		)
		Label(parent, text='Трапеции').grid(
			row=2, column=0, padx=5, pady=5,
		)
		Label(parent, text='Симпсон').grid(
			row=3, column=0, padx=5, pady=5,
		)
		Label(parent, text='Nmin').grid(
			row=4, column=0, padx=5, pady=5,
		)
		Entry(parent,
		      textvariable=self.results['left_rectangle'],
		      state='readonly').grid(
			row=0, column=1, padx=5, pady=5
		)
		Entry(parent,
		      textvariable=self.results['right_rectangle'],
		      state='readonly').grid(
			row=1, column=1, padx=5, pady=5
		)
		Entry(parent,
		      textvariable=self.results['trapezoidal'],
		      state='readonly').grid(
			row=2, column=1, padx=5, pady=5
		)
		Entry(parent, textvariable=self.results['simpson_rule'],
		      state='readonly').grid(
			row=3, column=1, padx=5, pady=5
		)
		Entry(parent, textvariable=self.results['min_common_step'],
		      state='readonly').grid(
			row=4, column=1, padx=5, pady=5
		)
		Button(parent, text='Метод Рунге',
		       command=self.main_app.open_runge).grid(
			row=5, column=0, padx=5, pady=5
		)


	def notdone(self):
		pass


class RungeRuleFrame(Frame):
	def __init__(self, main_frame, main_app):
		Frame.__init__(self, main_frame)
		self.main_app = main_app
		self.make_widgets()

	def make_widgets(self):
		self.input_area_frame = Frame(self)
		self.graph_area_frame = Frame(self)
		self.bottom_frame = Frame(self)
		self.bottom_frame.pack(side=BOTTOM, fill=X)
		self.pick_integral_frame = Frame(self.input_area_frame)
		self.input_num_frame = Frame(self.input_area_frame)
		self.output_num_frame = Frame(self.bottom_frame)
		self.input_area_frame.pack(side=LEFT, anchor=NW)
		self.graph_area_frame.pack(side=RIGHT, anchor=NE)
		self.pick_integral_frame.pack(side=TOP, anchor=NW)
		self.input_num_frame.pack(side=TOP, anchor=W)
		self.output_num_frame.pack(side=LEFT, fill=X, anchor=W)

		self.selected_integral = IntVar()
		self.selected_integral.set(1)

		self.img1 = Image.open('integral_1.png')
		self.img2 = Image.open('integral_2.png')
		self.photo1 = ImageTk.PhotoImage(self.img1)
		self.photo2 = ImageTk.PhotoImage(self.img2)

		Radiobutton(self.pick_integral_frame,
		                       text='1',
		                       variable=self.selected_integral,
		                       value=1).grid(
			row=0, column=0, padx=5, pady=5
		)
		Radiobutton(self.pick_integral_frame,
		                       text='2',
		                       variable=self.selected_integral,
		                       value=2).grid(
			row=1, column=0, padx=5, pady=5
		)

		Label(self.pick_integral_frame,
		      image=self.photo1).grid(row=0, column=1, padx=5, pady=5)
		Label(self.pick_integral_frame,
		      image=self.photo2).grid(row=1, column=1, padx=5, pady=5)


		Label(self.input_num_frame, text='a').grid(row=0, column=0, padx=5, pady=5)
		Label(self.input_num_frame, text='b').grid(row=1, column=0, padx=5, pady=5)
		Label(self.input_num_frame, text='n').grid(row=2, column=0, padx=5, pady=5)
		Label(self.input_num_frame, text='Точность').grid(row=3, column=0, padx=5, pady=5)

		self.lower = StringVar()
		self.upper = StringVar()
		self.stride = StringVar()
		self.tolerance = StringVar()

		Entry(self.input_num_frame, textvariable=self.lower).grid(row=0, column=1, padx=5, pady=5)
		Entry(self.input_num_frame, textvariable=self.upper).grid(row=1, column=1, padx=5, pady=5)
		Entry(self.input_num_frame, textvariable=self.stride).grid(row=2, column=1, padx=5, pady=5)
		Entry(self.input_num_frame, textvariable=self.tolerance).grid(
			row=3, column=1, padx=5, pady=5
		)

		Button(self.input_num_frame, text='Запустить ракету',
		                  command=self.printer).grid(row=4, column=0,
		                                             padx=5, pady=5)

		self.results = {}
		self.results['left_rectangle_I_n'] = StringVar()
		self.results['right_rectangle_I_n'] = StringVar()
		self.results['trapezoidal_I_n'] = StringVar()
		self.results['simpson_rule_I_n'] = StringVar()
		self.results['left_rectangle_I_2n'] = StringVar()
		self.results['right_rectangle_I_2n'] = StringVar()
		self.results['trapezoidal_I_2n'] = StringVar()
		self.results['simpson_rule_I_2n'] = StringVar()
		self.results['left_rectangle_n'] = StringVar()
		self.results['right_rectangle_n'] = StringVar()
		self.results['trapezoidal_n'] = StringVar()
		self.results['simpson_rule_n'] = StringVar()
		self.make_output(self.output_num_frame)

		self.fig = plt.figure(figsize=(4, 3), dpi=100)
		self.ax = self.fig.add_subplot(111)
		self.ax.set_title("Пустой график")

		self.canvas = FigureCanvasTkAgg(self.fig,
		                                master=self.graph_area_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(
			side=TOP,
			anchor='ne',
			padx=10,
			pady=10
		)

	def printer(self):
		try:
			params = self.get_input()
			results = self.calculate_integrals(params)
			self.update_results(results)
			self.update_plot(params)


		except EmptyInput as e:
			messagebox.showerror(
				"Ошибка ввода",
				e
			)

		except StepError as e:
			messagebox.showerror(
				"Ошибка шага",
				e
			)

		except DomainError:
			messagebox.showerror(
				"Ошибка области определения",
				"Функция не определена на данном интервале"
			)

		except ZeroDenominatorError:
			messagebox.showerror(
				"Деление на ноль",
				"Знаменатель обращается в ноль"
			)

		except NonNumInput as e:
			messagebox.showerror(
				"Ошибка ввода",
				e
			)

		except EvenStepWarning as e:
			messagebox.showerror(
				'Нечетное разбиение',
				'Simpson rule requires even n'
			)

		except Exception as e:
			messagebox.showerror(
				"Неизвестная ошибка",
				f'Упс...\nВы нашли ошибку, которую я не '
				f'предусмотел!\n\nПожалуйста, напишите о ней на почту нашего '
				f'разработчика antonsu-spb@yandex.ru и мы обязательно учтем '
				f'её в следующем релизе!\n\nP.S. Ошибка, с которой вы '
				f'столкнулись: {e}'
			)


	def get_input(self):
		a = self.lower.get()
		b = self.upper.get()
		n = self.stride.get()
		tolerance = self.tolerance.get()

		if self.selected_integral.get() == 1:
			func = integrals.function_1
		elif self.selected_integral.get() == 2:
			func = integrals.function_2

		return func, a, b, n, tolerance

	def calculate_integrals(self, input_data):
		return {
			'left_rectangle': integrals.runge_rule(
				integrals.left_rectangle, *input_data
			),
			'right_rectangle': integrals.runge_rule(
				integrals.right_rectangle, *input_data
			),
			'trapezoidal': integrals.runge_rule(
				integrals.trapezoidal, *input_data
			),
			'simpson_rule': integrals.runge_rule(
				integrals.simpson_rule, *input_data
			),
		}

	def update_results(self, results: dict):
		for key in results:
			self.results[key + '_I_n'].set(results[key]['I_n'])
			self.results[key + '_I_2n'].set(results[key]['I_2n'])
			self.results[key + '_n'].set(results[key]['n'])

	def update_plot(self, params):
		a, b, n, _ = params[1:]
		a, b, n = integrals.validate_input(a, b, n)
		func = params[0]
		MIN_PLOT_POINTS = 500
		n = max(MIN_PLOT_POINTS, n)

		self.ax.clear()
		x = np.linspace(a, b, n)
		y = func(x)

		self.ax.plot(x, y)
		self.canvas.draw()

	def make_output(self, parent):
		Label(parent, text='S левые').grid(
			row=1, column=0, padx=5, pady=5
		)
		Label(parent, text='S правые').grid(
			row=2, column=0, padx=5, pady=5,
		)
		Label(parent, text='S трап').grid(
			row=3, column=0, padx=5, pady=5,
		)
		Label(parent, text='S симпс').grid(
			row=4, column=0, padx=5, pady=5,
		)
		Label(parent, text='I_n').grid(
			row=0, column=1, padx=5, pady=5,
		)
		Label(parent, text='I_2n').grid(
			row=0, column=2, padx=5, pady=5,
		)
		Label(parent, text='n').grid(
			row=0, column=3, padx=5, pady=5,
		)
		Entry(parent,
		      textvariable=self.results['left_rectangle_I_n'],
		      state='readonly').grid(
			row=1, column=1, padx=5, pady=5
		)
		Entry(parent,
		      textvariable=self.results['right_rectangle_I_n'],
		      state='readonly').grid(
			row=2, column=1, padx=5, pady=5
		)
		Entry(parent,
		      textvariable=self.results['trapezoidal_I_n'],
		      state='readonly').grid(
			row=3, column=1, padx=5, pady=5
		)
		Entry(parent, textvariable=self.results['simpson_rule_I_n'],
		      state='readonly').grid(
			row=4, column=1, padx=5, pady=5
		)

		Entry(parent,
		      textvariable=self.results['left_rectangle_I_2n'],
		      state='readonly').grid(
			row=1, column=2, padx=5, pady=5
		)
		Entry(parent,
		      textvariable=self.results['right_rectangle_I_2n'],
		      state='readonly').grid(
			row=2, column=2, padx=5, pady=5
		)
		Entry(parent,
		      textvariable=self.results['trapezoidal_I_2n'],
		      state='readonly').grid(
			row=3, column=2, padx=5, pady=5
		)
		Entry(parent, textvariable=self.results['simpson_rule_I_2n'],
		      state='readonly').grid(
			row=4, column=2, padx=5, pady=5
		)

		Entry(parent,
		      textvariable=self.results['left_rectangle_n'],
		      state='readonly').grid(
			row=1, column=3, padx=5, pady=5
		)
		Entry(parent,
		      textvariable=self.results['right_rectangle_n'],
		      state='readonly').grid(
			row=2, column=3, padx=5, pady=5
		)
		Entry(parent,
		      textvariable=self.results['trapezoidal_n'],
		      state='readonly').grid(
			row=3, column=3, padx=5, pady=5
		)
		Entry(parent, textvariable=self.results['simpson_rule_n'],
		      state='readonly').grid(
			row=4, column=3, padx=5, pady=5
		)
		Button(parent, text='< назад', fg='red',
		       command=self.main_app.open_integrals).grid(
			row=4, column=4, padx=5, pady=5
		)

class RootFindingFrame(Frame):
	def __init__(self, main_frame, main_app):
		Frame.__init__(self, main_frame)
		self.make_widgets()
		self.main_app = main_app
	def make_widgets(self):
		self.test_text = Label(self, text="Here'll be some Nonlinear "
		                                  "Equations stuff")
		self.test_text.pack(expand=True, fill=BOTH)

class ApproximationFrame(Frame):
	def __init__(self, main_frame, main_app):
		Frame.__init__(self, main_frame)
		self.make_widgets()
		self.main_app = main_app
	def make_widgets(self):
		self.test_text = Label(self, text="Here'll be some approximation "
		                                  "stuff")
		self.test_text.pack(expand=True, fill=BOTH)

class InterpolationFrame(Frame):
	def __init__(self, main_frame, main_app):
		Frame.__init__(self, main_frame)
		self.make_widgets()
		self.main_app = main_app
	def make_widgets(self):
		self.test_text = Label(self, text="Here'll be some Interpolation "
		                                  "stuff")
		self.test_text.pack(expand=True, fill=BOTH)

class DifferentialEquationFrame(Frame):
	def __init__(self, main_frame, main_app):
		Frame.__init__(self, main_frame)
		self.make_widgets()
		self.main_app = main_app
	def make_widgets(self):
		self.test_text = Label(self, text="Here'll be some "
		                                  "differential equations stuff")
		self.test_text.pack(expand=True, fill=BOTH)

if __name__ == "__main__":
    app = MainApp()
    app.run()