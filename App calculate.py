import tkinter as tk


class Calculator:
	def __init__(self, root):
		self.root = root
		self.expression = ""

		root.title("Simple Calculator")
		root.geometry("340x470")
		root.minsize(300, 420)
		root.configure(bg="#18212b")

		self.display = tk.StringVar(value="0")
		screen = tk.Entry(
			root,
			textvariable=self.display,
			font=("Segoe UI", 30),
			justify="right",
			state="readonly",
			readonlybackground="#18212b",
			fg="#f4f7fa",
			bd=0,
			highlightthickness=0,
		)
		screen.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=18, pady=(24, 18), ipady=12)

		buttons = [
			("C", "#d66a62"), ("⌫", "#344351"), ("÷", "#344351"), ("×", "#344351"),
			("7", "#25313d"), ("8", "#25313d"), ("9", "#25313d"), ("−", "#344351"),
			("4", "#25313d"), ("5", "#25313d"), ("6", "#25313d"), ("+", "#344351"),
			("1", "#25313d"), ("2", "#25313d"), ("3", "#25313d"), ("=", "#299a83"),
			("±", "#344351"), ("0", "#25313d"), (".", "#25313d"),
		]

		for column in range(4):
			root.grid_columnconfigure(column, weight=1, uniform="column")
		for row in range(1, 6):
			root.grid_rowconfigure(row, weight=1, uniform="row")

		for index, (label, color) in enumerate(buttons):
			row = index // 4 + 1
			column = index % 4
			button = tk.Button(
				root,
				text=label,
				font=("Segoe UI", 18, "bold"),
				bg=color,
				fg="#ffffff",
				activebackground="#526273",
				activeforeground="#ffffff",
				bd=0,
				cursor="hand2",
				command=lambda value=label: self.press(value),
			)
			if label == "=":
				button.grid(row=row, column=column, rowspan=2, sticky="nsew", padx=5, pady=5)
			else:
				button.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)

		root.bind("<Key>", self.handle_key)

	def press(self, value):
		if value == "C":
			self.expression = ""
		elif value == "⌫":
			self.expression = self.expression[:-1]
		elif value == "=":
			self.calculate()
			return
		elif value == "±":
			if self.expression and self.expression[0] == "-":
				self.expression = self.expression[1:]
			elif self.expression:
				self.expression = "-" + self.expression
		else:
			self.expression += {"÷": "/", "×": "*", "−": "-"}.get(value, value)

		self.display.set(self.expression or "0")

	def calculate(self):
		try:
			result = eval(self.expression, {"__builtins__": {}}, {})
			if not isinstance(result, (int, float)):
				raise ValueError
			self.expression = str(int(result)) if result == int(result) else str(result)
			self.display.set(self.expression)
		except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
			self.expression = ""
			self.display.set("Error")

	def handle_key(self, event):
		if event.char in "0123456789.+-*/":
			self.press(event.char)
		elif event.keysym in ("Return", "KP_Enter"):
			self.calculate()
		elif event.keysym == "BackSpace":
			self.press("⌫")
		elif event.keysym == "Escape":
			self.press("C")


if __name__ == "__main__":
	window = tk.Tk()
	Calculator(window)
	window.mainloop()
