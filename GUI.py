import tkinter as tk
from tkinter import ttk
import subprocess
import difflib
import datetime
import os

# global vars
LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
fablesFile = open("fables.txt")
fables = fablesFile.read().split('\n\n')
fablesFile.close()
fableCount = 0
ID = None
Keylogger = None

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

		for fr in (PageStart, PageFinished):
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

	# sets up ID, directory, and takes user to next page
	def enrollUser(self, controller):
		uid = self.session.get()
		my_year = datetime.datetime.now().year
		julian = datetime.datetime.now().timetuple().tm_yday

		# final string to produce primary key
		global ID
		ID = "data/"+str(my_year) + "-" + str(julian) + "-"+ str(uid).zfill(3) + '.log'

		if(os.path.exists(ID)) == False:
			file = open(ID, 'w+')
			file.write("Log for: "+self.user.get()+"\n")
			file.close()
			controller.create_other_pages(controller.container,PageEnroll)
			controller.show_frame(PageEnroll)

		else:
			print("It appears this session already exists...")

# start page UI (landing page)
class PageEnroll(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		print(ID)
		self.keylogProcess = subprocess.Popen(['python3', 'keylogger.py', ID])

		self.fableText = tk.Label(self, text = fables[fableCount])
		self.fableText.pack(pady=10, padx=10)

		self.collect = tk.Entry(self, width=50)
		self.collect.pack()
		self.collect.focus_set()

		self.submit =  tk.Button(self, text = "Submit", command = lambda: self.submitText(controller))
		self.submit.pack(pady=10, padx=10)

		self.incorrect = tk.Label(self, text=" ")
		self.incorrect.pack()

	def submitText(self, controller):
		check = self.collect.get()
		if check == fables[fableCount].replace('\n', ' '):
			self.updateFable(controller)
		else:
			self.incorrect.config(text="Check your typing. There might be a typo.")
			print(check)
			print(fables[fableCount].replace('\n', ' '))
			for i,s in enumerate(difflib.ndiff(check, fables[fableCount].replace('\n', ' '))):
				if s[0]==' ':
					continue
				elif s[0]=='-':
					print(u'Delete "{}" from position {}'.format(s[-1],i))
				elif s[0]=='+':
					print(u'Add "{}" to position {}'.format(s[-1],i))    
			print()

	def updateFable(self, controller):
		global fableCount
		if fableCount < 3:
			fableCount += 1
			self.fableText.config(text=fables[fableCount])
			self.collect.delete(0, 'end')
			self.incorrect.config(text="")
		else:
			if(self.keylogProcess.poll()==None):
				self.keylogProcess.kill()
			controller.show_frame(PageFinished)

# start page UI (landing page)
class PageFinished(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		finished = tk.Label(self, text="You have finished enrollment!")
		finished.pack(pady=50)

# global commands for debugging use
def addCommand():
	print("Need to add a command here")

app = KeyloggerGUI() # initialize app
app.geometry("%dx%d" % (800, 400)) # set window dimensions

app.mainloop()