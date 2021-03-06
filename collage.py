import sys
import matplotlib
matplotlib.use('TkAgg')
try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
from notebook import *   # window with tabs
from ADPCX_GUI_frame import *

root = Tk( ) 
root.title('ADPCX')
nb = notebook(root, TOP) # make a few diverse frames (panels), each using the NB as 'master': 

# uses the notebook's frame
f1 = Frame(nb( )) 
dft = ADPCX_frame(f1)


nb.add_screen(f1, "") 

nb.display(f1)

root.geometry('+0+0')
root.mainloop( )
