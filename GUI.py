import tkinter as tk
from tkinter import ttk
import keylogger

LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
ID = None

class KeyloggerGUI(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, "User Keystroke Identifier")

		self.container = tk.Frame(self)

		self.container.pack(side="top", fill="both", expand=True)

		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		#initialize arbitrary pages

		for fr in (PageStart, PageEnroll):
			frame = fr(self.container, self)
			self.frames[fr] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(PageStart)

		# raises page of interest
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.grid(row=0, column=0, sticky="nsew")
		frame.tkraise()

	# create rest of pages (only able to call after ID has been created)
	def create_other_pages(self, container, page):
		frame = page(self.container, self)
		self.frames[page] = frame

# start page UI (landing page)
class PageStart(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text = "User Keylogging Collection", font = LARGE_FONT)
		label.pack(pady=10, padx=10)

		label = tk.Label(self, text = "Enter Session ID:", font = MEDIUM_FONT)
		label.pack()

		self.session = tk.Entry(self)
		self.session.pack(pady=20)
		self.session.focus_set()

		label = tk.Label(self, text = "Enter Your Full Name:", font = MEDIUM_FONT)
		label.pack()

		self.user = tk.Entry(self)
		self.user.pack(pady=20)
		self.user.focus_set()

		button2d = ttk.Button(self, text = "Enrollment", command = lambda: self.enrollUser(controller))
		button2d.pack()

		button2d = ttk.Button(self, text = "Identification", command = lambda: self.identifyUser(controller))
		button2d.pack()

		finishButton = ttk.Button(self, text = "Cancel", command = lambda: self.quit)
		finishButton.pack(pady=10)

# start page UI (landing page)
class PageEnroll(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)


# global commands for debugging use
def addCommand():
	print("Need to add a command here")

app = KeyloggerGUI() # initialize app
app.geometry("%dx%d" % (800, 400)) # set window dimensions

app.mainloop()