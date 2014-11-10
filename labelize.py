import os
import re
from mutagen.easyid3 import EasyID3

import Tkinter, tkFileDialog, tkSimpleDialog, tkMessageBox
from Tkinter import *
formats = r"(mp3|aac|mp4|aiff|flac|wav)$"

global rootDir 
def init():
	init_ui()
	mainloop()


def labelize(dir, run_simulation):
	text.delete("1.0", END)

	output = ""
	for label in os.listdir(dir):
		if not re.match(r"^\.",label):
			output += label + ":\n"
			text.insert('end', label + ":\n")
			for parent, subdirs, file in os.walk(dir+"/"+label):
				all_files = filter_files([os.path.join(parent, f) for f in os.listdir(parent)])
				for f in all_files:
					filename = f.split('/')[-1]
					output += "    "
					text.insert('end', "    ")
					output += filename
					text.insert('end', filename)
					output += "\n"
					text.insert('end', "\n")
					if not run_simulation:
						set_label_to(f, label)
	print output



def run_as_simulation():
	labelize(rootDir, True)
def run_normal():
	labelize(rootDir, False)
def filter_files(file_list):
 	return [file for file in file_list if isSong(file)]

def display_directory_dialog():
	global rootDir 
	rootDir = tkFileDialog.askdirectory(parent=root,initialdir="~/dev/label-tagger/test",title='Please select a directory')
	labels = os.listdir(rootDir)
	text.insert('end', "Will traverse each of the following folders, and apply the publisher tag:\n")
	for label in labels:
		if not re.match(r"^\.", label):
			text.insert('end', "  "+label+"\n")

def init_ui():
	global root

	root = Tkinter.Tk()
	global run_simulation
	global text
	buttons = Frame(root).pack(side=RIGHT)
	Button(buttons, text="Select Folder", command=display_directory_dialog).pack(side=LEFT)
	Button(buttons, text="Simulate", command=run_as_simulation).pack(side=LEFT)
	Button(buttons, text="Run", command=run_normal).pack(side=LEFT)
	Button(buttons, text="Quit", command=exit).pack(side=LEFT)

	output = Frame(root).pack(side=BOTTOM)
	text = Text(output)
	text.pack(side=TOP)

def set_label_to(file, label_name):
	tags = EasyID3(file)
	EasyID3.RegisterTextKey('publisher', 'TPUB')
	tags['publisher'] = unicode(label_name)
	tags.save()
	return

def isSong(file):
	if re.search(formats, file):
		return True

init()
main(text)