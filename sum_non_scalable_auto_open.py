#!/usr/bin/env python
import os
import sys
import csv
import Tkinter as tk
from tkFileDialog import askopenfile
from tkFileDialog import asksaveasfilename

assembly_num = ''
file_path = ''
output = 0
csv_input = 'AC-90, Total qty\n '

def find_sum(input_file, assembly_num):
    with open(input_file, 'rb') as file:
        reader = csv.reader(file)
        sum = 0
        for row in reader:
            if ( int(row[3]) == int(assembly_num)):
                sum += int(row[19])
    return sum

def find_summary(input_file):
	result = 0
	global csv_input
	for index in range(11):
		a =find_sum(input_file, index+1)
		result = result + a
		csv_input+=str(index+1) + ', ' + str(a) + '\n'

	csv_input+='Total, ' + str(result) 
	return result;

class Application(tk.Frame):

	global assembly_num
	global model_num
	global file_path

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid(sticky = tk.N+tk.S+tk.E+tk.W)
		self.createWidgets()
				


	def createWidgets(self):		
		self.grid(padx=2, pady=2)
		self.canvas = tk.Canvas(self, height = 310, border = 5, relief = "groove", bg = 'white')
		self.canvas.grid(column = 7, row = 0, rowspan = 21, columnspan = 14)
		self.canvas.create_text(50, 50, text ="\t\t\t1. Upload file.\n\t\t\t2. Select machine number.\n", font = "Pursia, 11", justify = tk.LEFT)
		
		def upload_file():
			global file_path
			file_path = askopenfile(mode ='r').name
			self.canvas.delete("all")
			self.canvas.create_text(50, 90, text ="\t\t\tFile selected", font = "Pursia, 12", justify = tk.LEFT)
			print file_path

		def reset():
			global file_path
			global assembly_num
			file_path = ''
			assembly_num = ''

			for index in range(11):
				assembly_buttons[index].deselect()

			self.canvas.delete("all")
			self.canvas.create_text(50, 50, text ="\t\t\t1. Upload file.\n\t\t\t2. Select machine number.\n", font = "Pursia, 12", justify = tk.LEFT)
			print 'reset'

		def ButtonClick():
			global assembly_num
			global file_path
			assembly_num = self.assem.get()
			model_num = self.modl.get()
			print 'assembly: ' + str(assembly_num)
			print 'model: ' + str(model_num)

			if(file_path != '' and assembly_num != 0):
				sum = find_sum(file_path, str(assembly_num))
				print 'Total units produced-> ' + str(sum)
				self.canvas.delete("all")
				self.canvas.create_text(110, 30, text ='Assembly number-> ' + str(assembly_num), font = "Pursia, 11")
				# self.canvas.create_text(110, 50, text ='Model number-> ' + str(model_num), font = "Pursia, 11")
				self.canvas.create_text(110, 70, text ='Total units produced-> ' + str(sum), font = "Pursia, 11")
			else:
				self.canvas.delete("all")
				if(file_path=='' and assembly_num == ''):
			 		self.canvas.create_text(50, 50, text ="\t\tFile and assembly not selected!", font = "Pursia, 12", justify = tk.LEFT)
				elif(assembly_num==''):
					self.canvas.create_text(20, 70, text ="\t\tAssembly_num not selected!", font = "Pursia, 12", justify = tk.LEFT)
				elif(file_path==''):
				 	self.canvas.create_text(20, 70, text ="\t\tFile path not selected!", font = "Pursia, 12", justify = tk.LEFT)

		def summary():
			global csv_input
			global file_path
			self.canvas.delete("all")

			if(file_path != ''):
				result = 0
				for index in range(11):
					a = find_sum(file_path, index+1)
					result += a
					self.canvas.create_text(110, 30+19*index, text ='Assembly ' + str(index+1) + ': ' + str(a), font = "Pursia, 11")
				self.canvas.create_text(110, 240, text ='Total output-> ' + str(result), font = "Pursia, 14")
			
			else:
				self.canvas.create_text(20, 70, text ="\t\tFile path not selected!", font = "Pursia, 12", justify = tk.LEFT)

		def toCSV():
			self.canvas.delete("all")
			global csv_input
			global file_path
			

			if(file_path != ''):
				res = find_summary(file_path)
				#print csv_input
				file_write = asksaveasfilename(defaultextension = '.csv')
				with open(file_write, 'w') as csvfile:
					csvfile.write(csv_input)
				csvfile.close()			
				self.canvas.create_text(20, 70, text ="\t\tFile exported to CSV", font = "Pursia, 12", justify = tk.LEFT)
				self.canvas.create_text(20, 90, text ="\t\tOpening file...", font = "Pursia, 12", justify = tk.LEFT)
				os.system("start " + file_write)
				csv_input = ''
			else:
				self.canvas.create_text(20, 70, text ="\t\tFile path not selected!", font = "Pursia, 12", justify = tk.LEFT)


		top = self.winfo_toplevel()
		top.rowconfigure(0, weight = 1)
		top.columnconfigure(0, weight = 1)
		top = self.winfo_toplevel()
		self.menuBar = tk.Menu(top)
		top['menu'] = self.menuBar
		self.subMenu = tk.Menu(self.menuBar)
		self.subMenu1 = tk.Menu(self.menuBar)
		self.menuBar.add_cascade(label='File', menu=self.subMenu)
		self.subMenu.add_command(label='About')
		self.subMenu.add_command(label = 'Exit', command=self.quit)
		self.menuBar.add_cascade(label='Help', menu=self.subMenu1)	


		self.assem = tk.StringVar()
		self.modl = tk.StringVar()	

		assembly_buttons = []
		for index in range(11):
			button = tk.Radiobutton(self, border = 3, relief = "groove", variable=self.assem, value=(index+1), text = "AC-90#" + str(index+1), indicatoron = 0)
			button.grid(column = 0, row = 1+index*3, padx = 5, pady = 5, rowspan = 3,ipadx = 5, ipady = 5)
			button["command"] = ButtonClick
			assembly_buttons.append(button)

		self.label2 = tk.Label(self, text ="Assembly no.")
		self.label2.grid(column = 0, row = 0)

		self.summaryButton = tk.Button(self, border = 3, relief = "groove" , text = 'Summary')
		self.summaryButton["command"] = summary
		self.summaryButton.grid(column = 20, row = 25, rowspan = 3,ipadx = 15, ipady = 5)

		self.toCsvButton = tk.Button(self, border = 3, relief = "groove" , text = 'Export to\n CSV')
		self.toCsvButton["command"] = toCSV
		self.toCsvButton.grid(column = 20, row = 22, rowspan = 3,ipadx = 15, ipady = 5)

		
		self.uploadButton = tk.Button(self, foreground = 'green', border = 3, relief = "groove" , text = 'Upload CSV')
		self.uploadButton["command"] = upload_file
		self.uploadButton.grid(column = 17, row = 31, padx = 5, pady = 5, rowspan = 3,ipadx = 35, ipady = 5,columnspan = 3)

		self.resetButton = tk.Button(self,justify = tk.CENTER, foreground = 'blue', command = reset, border = 3, relief = "groove",text = 'Reset')
		self.resetButton.grid(column = 20, row = 28,  padx = 0, pady = 1, rowspan = 3,ipadx = 27, ipady = 5)

		self.exitButton = tk.Button(self, foreground = 'red', justify = tk.CENTER, border = 3, relief = "groove",text = 'Exit', command = self.quit)
		self.exitButton.grid(column = 20, row = 31,  padx = 0, pady = 1, rowspan = 3,ipadx = 32, ipady = 5)



app = Application()
app.master.title('Yazaki_AC-90')
app.master.minsize(width=490, height=560)
app.master.maxsize(width=490, height=560)
app.mainloop()
