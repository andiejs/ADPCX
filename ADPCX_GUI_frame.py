try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
    import tkFileDialog, tkMessageBox
except ImportError:
    # for Python3
    from tkinter import *  ## notice lowercase 't' in tkinter here
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox
import sys, os, tempfile
import numpy as np
from matplotlib import pyplot as plt
import ADPCX
import PIL
from PIL import Image

class ADPCX_frame:
	temp_path = os.path.join(tempfile.gettempdir(),"adpcx.png")
	alpha_path = os.path.join(tempfile.gettempdir(),"alphachannel.png")
	#temp_path = "/tmp/foo.png"
	#alpha_path = "/tmp/alphachannel.png"   
	def __init__(self, parent):  
		 
		self.parent = parent        
		self.initUI()

	def initUI(self):
		initialdir = "~/"
		default_image_1 = 'gold.jpeg'
		default_image_2 = 'brood.jpeg'
		#TEXTBOX TO PRINT PATH OF THE FILE
		self.filelocation = Entry(self.parent)
		self.filelocation.focus_set()
		self.filelocation["width"] = 67
		self.filelocation.grid(row=1,column=0, sticky=W, padx=10)
		self.filelocation.delete(0, END)
		self.filelocation.insert(0, default_image_1)

		#BUTTON TO BROWSE FILE
		self.open_file = Button(self.parent, text="Browse 1...", command=self.browse_file) #see: def browse_file(self)
		self.open_file.grid(row=1, column=0, sticky=W, padx=(1060, 6)) #put it beside the filelocation textbox
 
		#BUTTON TO PREVIEW FILE
#		self.preview = Button(self.parent, text=">", command=lambda:self.show_image(self.filelocation.get(),"image1"), bg="gray30", fg="white")
#		self.preview.grid(row=1, column=0, sticky=W, padx=(306 + 100,6))





		self.filelocation2 = Entry(self.parent)
		self.filelocation2.focus_set()
		self.filelocation2["width"] = 67
		self.filelocation2.grid(row=2,column=0, sticky=W, padx=10)
		self.filelocation2.delete(0, END)
		self.filelocation2.insert(0, default_image_2)

		#BUTTON TO BROWSE FILE
		self.open_file = Button(self.parent, text="Browse 2...", command=self.browse_file2) #see: def browse_file(self)
		self.open_file.grid(row=2, column=0, sticky=W, padx=(1060, 6)) #put it beside the filelocation textbox
 
		#BUTTON TO PREVIEW FILE
#		self.preview = Button(self.parent, text=">", command=lambda:self.show_image(self.filelocation2.get(),"image2"), bg="gray30", fg="white")
#		self.preview.grid(row=2, column=0, sticky=W, padx=(406,6))

		Label(self.parent, text="Img1 coords:").grid(row=3, column=0, sticky=W, padx=5, pady=(10,2))
		self.Ax = Entry(self.parent, justify=CENTER)
		self.Ax["width"] = 5
		self.Ax.grid(row=3,column=0, sticky=W, padx=(185,5), pady=(10,2))
		self.Ax.delete(0, END)
		self.Ax.insert(0, "0")
		self.Ay = Entry(self.parent, justify=CENTER)
		self.Ay["width"] = 5
		self.Ay.grid(row=3,column=0, sticky=W, padx=(285,5), pady=(10,2))
		self.Ay.delete(0, END)
		self.Ay.insert(0, "0")

		Label(self.parent, text="Img2 coords:").grid(row=4, column=0, sticky=W, padx=5, pady=(10,2))
		self.Bx = Entry(self.parent, justify=CENTER)
		self.Bx["width"] = 5
		self.Bx.grid(row=4,column=0, sticky=W, padx=(185,5), pady=(10,2))
		self.Bx.delete(0, END)
		self.Bx.insert(0, "0")
		self.By = Entry(self.parent, justify=CENTER)
		self.By["width"] = 5

		self.By.grid(row=4,column=0, sticky=W, padx=(285,5), pady=(10,2))
		self.By.delete(0, END)
		self.By.insert(0, "0")


		Label(self.parent, text="Cutoff:").grid(row=5, column=0, sticky=W, padx=5, pady=(10,2))
		self.M = Entry(self.parent, justify=CENTER)
		self.M["width"] = 5
		self.M.grid(row=5,column=0, sticky=W, padx=(105,5), pady=(10,2))
		self.M.delete(0, END)
		self.M.insert(0, "100")


	
		#BUTTON TO COMPUTE EVERYTHING
		self.compute = Button(self.parent, text="Compute", command=self.compute_model, bg="dark red", fg="white")
		self.compute.grid(row=6, column=0, padx=5, pady=(10,15), sticky=W)

		self.compute = Button(self.parent, text="Preview", command=self.show_four, bg="dark red", fg="white")
		self.compute.grid(row=7, column=0, padx=5, pady=(10,15), sticky=W)

		self.save = Button(self.parent, text="Save", command=self.save, bg="dark red", fg="white")
		self.save.grid(row=8, column=0, padx=5, pady=(10,15), sticky=W)



		# define options for opening file
		self.file_opt = options = {}
		#options['defaultextension'] = '.wav'
		#options['filetypes'] = [('All files', '.*'), ('Wav files', '.wav')]
		options['initialdir'] = initialdir
		options['title'] = 'Open an impage file'

	def show_image(self,path,title):
		im = Image.open(path)
		im.show(title=title)

	def browse_file(self):
		
		self.filename = tkFileDialog.askopenfilename(**self.file_opt)
 
		#set the text of the self.filelocation
		self.filelocation.delete(0, END)
		self.filelocation.insert(0,self.filename)
		self.file_opt['initialdir'] = os.path.dirname(self.filename)

	def browse_file2(self):
		
		self.filename2 = tkFileDialog.askopenfilename(**self.file_opt)
 
		#set the text of the self.filelocation
		self.filelocation2.delete(0, END)
		self.filelocation2.insert(0,self.filename2)
		self.file_opt['initialdir'] = os.path.dirname(self.filename2)


	def compute_model(self):
		
		try:
			inputFile = self.filelocation.get()
			inputFile2 = self.filelocation2.get()
			cutoff = int(self.M.get())
			ax = int(self.Ax.get())
			ay = int(self.Ay.get())
			bx = int(self.Bx.get())
			by = int(self.By.get())
			ADPCX.do_it(inputFile,inputFile2,self.temp_path,self.alpha_path,cutoff,ax,ay,bx,by)


		except ValueError as errorMessage:
			tkMessageBox.showerror("Input values error",errorMessage)
			

	def save(self):
		name=tkFileDialog.asksaveasfile(mode='wb',defaultextension=".png",initialdir="images/")
		im = Image.open(self.temp_path)
		im.save(name,format='png')

	def show_four(self):  
# create figure
		fig = plt.figure(figsize=(10, 7))

# setting values to rows and column variables
		rows = 2
		columns = 2

# reading images
		Image1 = np.array(Image.open(self.filelocation.get()))
		Image2 = np.array(Image.open(self.filelocation2.get()))
		Image3 = Image.open(self.alpha_path)
		Image4 = np.array(Image.open(self.temp_path))

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
		plt.imshow(Image4)
		plt.axis('off')
		plt.title("Result")


		plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.0, hspace=0.12)
                # showing image
		plt.show()
