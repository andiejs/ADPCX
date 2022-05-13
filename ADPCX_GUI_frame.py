# GUI frame for the dftModel_function.py

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
    import tkFileDialog, tkMessageBox
except ImportError:
    # for Python3
    from tkinter import *  ## notice lowercase 't' in tkinter here
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox
import sys, os
import numpy as np
#from scipy.io.wavfile import read
#import dftModel_function
#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))
#import utilFunctions as UF
from matplotlib import pyplot as plt
import ADPCX
import PIL
from PIL import Image

class ADPCX_frame:
  
	def __init__(self, parent):  
		 
		self.parent = parent        
		self.initUI()

	def initUI(self):

		#TEXTBOX TO PRINT PATH OF THE FILE
		self.filelocation = Entry(self.parent)
		self.filelocation.focus_set()
		self.filelocation["width"] = 37
		self.filelocation.grid(row=1,column=0, sticky=W, padx=10)
		self.filelocation.delete(0, END)
		self.filelocation.insert(0, '/home/monster/Downloads/gold.jpeg')

		#BUTTON TO BROWSE FILE
		self.open_file = Button(self.parent, text="Browse...", command=self.browse_file) #see: def browse_file(self)
		self.open_file.grid(row=1, column=0, sticky=W, padx=(220 + 100, 6)) #put it beside the filelocation textbox
 
		#BUTTON TO PREVIEW FILE
#		self.preview = Button(self.parent, text=">", command=lambda:self.show_image(self.filelocation.get(),"image1"), bg="gray30", fg="white")
#		self.preview.grid(row=1, column=0, sticky=W, padx=(306 + 100,6))





		self.filelocation2 = Entry(self.parent)
		self.filelocation2.focus_set()
		self.filelocation2["width"] = 37
		self.filelocation2.grid(row=2,column=0, sticky=W, padx=10)
		self.filelocation2.delete(0, END)
		self.filelocation2.insert(0, '/home/monster/Downloads/brood.jpeg')

		#BUTTON TO BROWSE FILE
		self.open_file = Button(self.parent, text="Browse...", command=self.browse_file2) #see: def browse_file(self)
		self.open_file.grid(row=2, column=0, sticky=W, padx=(320, 6)) #put it beside the filelocation textbox
 
		#BUTTON TO PREVIEW FILE
#		self.preview = Button(self.parent, text=">", command=lambda:self.show_image(self.filelocation2.get(),"image2"), bg="gray30", fg="white")
#		self.preview.grid(row=2, column=0, sticky=W, padx=(406,6))


		M_label = "Cutoff:"
		Label(self.parent, text=M_label).grid(row=3, column=0, sticky=W, padx=5, pady=(10,2))
		self.M = Entry(self.parent, justify=CENTER)
		self.M["width"] = 5
		self.M.grid(row=3,column=0, sticky=W, padx=(70,5), pady=(10,2))
		self.M.delete(0, END)
		self.M.insert(0, "100")





                
	
		#BUTTON TO COMPUTE EVERYTHING
		self.compute = Button(self.parent, text="Compute", command=self.compute_model, bg="dark red", fg="white")
		self.compute.grid(row=6, column=0, padx=5, pady=(10,15), sticky=W)

		# define options for opening file
		self.file_opt = options = {}
		#options['defaultextension'] = '.wav'
		#options['filetypes'] = [('All files', '.*'), ('Wav files', '.wav')]
		options['initialdir'] = '/home/monster/Downloads/'
		options['title'] = 'Open an impage file'

	def show_image(self,path,title):
		im = Image.open(path)
		im.show(title=title)

	def browse_file(self):
		
		self.filename = tkFileDialog.askopenfilename(**self.file_opt)
 
		#set the text of the self.filelocation
		self.filelocation.delete(0, END)
		self.filelocation.insert(0,self.filename)

	def browse_file2(self):
		
		self.filename2 = tkFileDialog.askopenfilename(**self.file_opt)
 
		#set the text of the self.filelocation
		self.filelocation.delete(0, END)
		self.filelocation.insert(0,self.filename2)

	def compute_model(self):
		
		try:
			inputFile = self.filelocation.get()
			inputFile2 = self.filelocation2.get()
			cutoff = int(self.M.get())
		#	N = int(self.N.get())
	#		time = float(self.time.get())
			ADPCX.do_it(inputFile,inputFile2,"/tmp/foo.png",cutoff)
			self.show_four()	
#			dftModel_function.main(inputFile, window, M, N, time)


		except ValueError as errorMessage:
			tkMessageBox.showerror("Input values error",errorMessage)
			


	def show_four(self):  
# create figure
		fig = plt.figure(figsize=(10, 7))

# setting values to rows and column variables
		rows = 2
		columns = 2

# reading images
		Image1 = np.array(Image.open(self.filelocation.get()))
		Image2 = np.array(Image.open(self.filelocation2.get()))
		Image3 = Image.open('/tmp/alphachannel.png')
		Image4 = np.array(Image.open('/tmp/foo.png'))

# Adds a subplot at the 1st position
		fig.add_subplot(rows, columns, 1)
# showing image
		plt.imshow(Image1)
		plt.axis('off')
		plt.title("Input 1")

# Adds a subplot at the 2nd position
		fig.add_subplot(rows, columns, 2)

# showing image
		plt.imshow(Image2)
		plt.axis('off')
		plt.title("Input 2")

# Adds a subplot at the 3rd position
		fig.add_subplot(rows, columns, 3)

# showing image
		plt.imshow(Image3)
		plt.axis('off')
		plt.title("Mask")

# Adds a subplot at the 4th position
		fig.add_subplot(rows, columns, 4)

# showing image
		plt.imshow(Image4)
		plt.axis('off')
		plt.title("Result")
		plt.show()
