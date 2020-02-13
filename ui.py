import Tkinter as tk
import ttk
from Tkinter import *



import serial
import RPi.GPIO as GPIO
import time

ser = serial.Serial('/dev/ttyACM0',9600)

		#plantId,stage,humidLow,humidHigh,tempLow,tempHigh
plantSettings = [
				[1,"Seedling",65.00,70.00,20.00,25.00],
				[2,"Vegitation",40.00,70.00,20.00,25.00],
				[3,"Blooming",40.00,50.00,20.00,25.00],
				]

plantStage = 'Seedling'
tempC = ''
humid = ''
class main:

	def __init__(self,root):
		#Window setup
		self.root=root
		self.root.title("AutoWeed64")
		self.root.geometry('800x600-30+30')
		
		#Window variables
		self.s = StringVar()
		self.h = StringVar()
		self.plantS = StringVar()
		self.happy = StringVar()

		self.root.configure(bg='white')

		#Menu bar
		menubar = Menu(self.root)
		self.root.config(menu=menubar)
		plantMenu = Menu(menubar)
		settingMenu = Menu(menubar)
		plantMenu.add_command(label="Exit")
		menubar.add_cascade(label="Plants", menu=plantMenu)
		menubar.add_cascade(label="Settings", menu=settingMenu)

		settingMenu.add_command(label="Open Settings", command=self.openSettings)

		#Labels
		root.grid_rowconfigure(1, weight=0)
		root.grid_columnconfigure(0, weight=1)
		top_frame = Frame(root, bg='white', width = 100, height=20, pady=12)
		top_frame.grid(row=0, sticky="ew")
		
		self.LABEL1 = Label(top_frame, text = 'Temperature: ', bg='white')
		self.LABEL1.grid(column=0,row=0)
		self.LABEL = Label(top_frame, text = '', textvariable = self.s, bg='white')
		self.LABEL.grid(column=1,row=0)
		self.LABEL2 = Label(top_frame, text = 'Humidity: ', bg='white')
		self.LABEL2.grid(column=2,row=0)
		self.LABEL3 = Label(top_frame, text = '', textvariable = self.h, bg='white')
		self.LABEL3.grid(column=3,row=0)
		self.root.after(1000, self.arduino)
		
		self.LABEL.config(font=(50))
		self.LABEL1.config(font=(50))
		self.LABEL2.config(font=(50))
		self.LABEL3.config(font=(50))
		
		
		#Tree
		center = Frame(root, bg='white', width=450, height=150)
		center.grid(row=1, sticky="ew")
		center.grid_rowconfigure(0, weight=1)
		center.grid_columnconfigure(1, weight=1)
		
		cols = ('PlantID', 'Stage', 'Moisture', 'Health')
		listBox = ttk.Treeview(center, columns=cols, show='headings')
		for col in cols:
			listBox.heading(col, text=col)    
			listBox.grid(row=1, column=0, columnspan=2)
		
		#Add plant	
		buttons = Frame(root, bg='white', width=450, height=50)
		buttons.grid_rowconfigure(0, weight=1)
		buttons.grid_columnconfigure(1, weight=1)
		add = Button(top_frame, text ="Hello")
		

#****************************************************************************************************
#****************************************************************************************************
#****************************************************************************************************
#****************************************************************************************************

	#Checking temperature and humidity
	def getHappy(self):
		if plantStage == 'Seedling':
			if humid>=65 and humid<=70:
				self.happy.set(':)')
			else:
				self.happy.set(':(')

	#Get sensor data from arduino and set the labels to display the data
	def arduino(self):
		tempC = ''
		humid = ''
		for x in range(10):
			if x <5:
				tempC = tempC + ser.read()
			else:
				humid = humid+ ser.read()

		self.s.set(tempC)
		self.h.set(humid)
		self.plantS.set(plantStage)
		self.getHappy
		self.root.after(1000,self.arduino)
		print tempC
		print humid
		self.root.update()


	#Setting window
	def openSettings(self):
		self.settings=settings
		self.settings.title("AutoWeed64 Settings")
		self.settings.geometry('800x600-30+30')
		settings = tk.Tk()
		
#Run the GUI
root = tk.Tk()
main(root)
root.mainloop()
ser.close()
