import time, colorama, re, os, threading, pyglet
from colorama import Fore
from datetime import datetime
from customtkinter import *
from customtkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from pygame import mixer
mixer.init()

pointless_score = 0 # Score for counter

# Calculating interval for countdown timer
# Reaches pointless score sound at around 63% through clip - divide by 100 to get time per point
tick = mixer.Sound('assets/countdown_timer.mp3').get_length()*0.63/100 

### CODE

def run(score):

	run_button.configure(state='disabled')

	if score == 'wrong':
		points_label.configure(text='❌')
		progbar.set(1)
		mixer.music.load('assets/counter_wrong.wav')
		mixer.music.play()
		threading.Thread(target=lambda: flash('wrong')).start()
		
	else:
		# Play countdown timer
		mixer.music.load('assets/countdown_timer.mp3')
		threading.Thread(target=mixer.music.play())

		# Loop through until score is reached
		for x in range(100-score): # loop until progress reaches score
			pointsvar.set(100-(x+1))
			points_label.configure(text=pointsvar.get())
			# progvar.set(100-(x+1)) # normal tkinter
			progbar.set((100-(x+1))/100) # CTk

			
			time.sleep(tick)

		# Play stop countdown sound if not a Pointless answer
		if score != 0:
			mixer.music.stop()
			mixer.music.load('assets/counter_stops1_3.wav')
			mixer.music.play()
		else:
			threading.Thread(target=lambda: flash('pointless')).start()

	# Set PlayerWidget score
	if score == 'wrong':
		score = 100
	current_widget.points += score
	current_widget.points_label.configure(text=current_widget.points)

	run_button.configure(state='normal')




###########
### GUI ###
###########



## Importing font
appdatalocal = os.getenv('LOCALAPPDATA')
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file('./assets/Baloo-Regular.ttf')
custom_font = 'Baloo'
custom_font_title = ('Baloo',60)


master = CTk()
master.geometry("1000x800")
master.title('Pointless')
set_default_color_theme('green')
rows = ['title', 'setpoints', 'points', 'progbar', 'run'] # Index of rows so I dont have to manually update each .grid

mainframe = CTkFrame(master, width=1000, height=800) # Split window in half for image on left side
mainframe.grid(row=0, column=0)

leftframe = CTkFrame(mainframe, width=600, height=600) # Left side - for image
leftframe.grid(row=1, column=0, padx=0, ipadx=0)

rightframe = CTkFrame(mainframe, height=600) # Right side - for GUI elements
rightframe.grid(row=1, column=1)

playersframe = CTkScrollableFrame(leftframe, width=600, height=600) # Left side - for image
playersframe.grid(row=0, column=0, padx=0, ipadx=0)


colourmain = '#8d73ff'
colourdark = '#5a49a4'


## Title
title_label = CTkLabel(mainframe, text=' POINTLESS ', font=custom_font_title, text_color=colourmain)
title_label.grid(row=0, column=0, sticky='nsew')



## Left Frame

# Focus event on click
# def focus(event):
# 	event.widget.focus_set()
# 	# print(master.focus_get())




players = [['Default', 0]]
current_widget = None

class PlayerWidget(CTkFrame):

	def __init__(self, parent, index):
		super().__init__(master=parent)

		self.name = players[index][0]
		self.points = players[index][1]

		self.name_entry = CTkEntry(self, width=550, height=20, font=(custom_font, 20), placeholder_text = 'Enter team name')
		self.name_entry.grid(row=0, column=0, padx=10, pady=10)

		self.points_label = CTkLabel(self, width=100, height=20, font=(custom_font, 20), text=self.points, padx=10)
		self.points_label.grid(row=1, column=0)

		self.grid(padx=10, pady=10, ipady=10)
		self.configure(border_width=5)

		# Bind clicking event to all widgets in class so you can click any of them to get focus
		for x in [self, self.name_entry, self.points_label]:
			x.bind('<FocusIn>', lambda event: self.configure(border_color='#fff'))
			x.bind('<FocusOut>', lambda event: self.configure(border_color='#000'))
			x.bind('<Button-1>', lambda event: event.widget.focus_set()) # Event when widget is clicked
			x.bind('<Button-1>', lambda event: self.click(index))
		

	# On click set currently selected widget
	def click(self, index):
		global current_widget
		current_widget = self
		players[index][0] = self.name_entry.get()
		

	# players[index].append(self)

# Initial player
initial_player = PlayerWidget(playersframe, 0)
current_widget = initial_player # Focus on default 
		
# Add player button

def addplayer():
	players.append(['Default', 0])
	PlayerWidget(playersframe, len(players)-1) # Index at next slot in list

addplayer_button = CTkButton(leftframe, text='Add player', font=(custom_font, 15), command=addplayer)
addplayer_button.grid(row=1, column=0)
	

## Right Frame

## Set Points
setpoints_frame = CTkFrame(rightframe)
setpoints_frame.grid(row=rows.index('setpoints'), column=0)

setpointsvar = ''

def addpoints(num):
	global setpointsvar
	setpointsvar = setpointsvar + str(num)

def setpoints(type=None):
	global setpointsvar, pointless_score

	if type == 'wrong':
		pointless_score = 'wrong'
	else:
		pointless_score = int(setpointsvar)
	print(pointless_score)
	setpointsvar = '' # reset setpointsvar

# Array of buttons
for x in range(10):
	numbutton = CTkButton(setpoints_frame, text=str(x), command=lambda x=x: addpoints(x), width=10) # https://stackoverflow.com/questions/18052395/array-of-buttons-in-python
	numbutton.grid(row=0, column=x)

spwrongbutton = CTkButton(setpoints_frame, text='X', command=lambda: setpoints('wrong'), fg_color='#ff0000', width=20)
spwrongbutton.grid(row=0, column=10)

spdonebutton = CTkButton(setpoints_frame, text='Set', command=setpoints, width=20)
spdonebutton.grid(row=0, column=11)

## Points

pointsvar = IntVar()
pointsvar.set(100)

points_label = CTkLabel(rightframe, text=pointsvar.get(), font=(custom_font, 30), text_color=colourmain, padx=10)
points_label.grid(row=rows.index('points'), column=0)

# ## Progress bar - normal tkinter
# global progvar
# progvar = IntVar()
# progvar.set(100)
# progbar = Progressbar(rightframe, orient=VERTICAL, length=500, mode='determinate', variable=progvar)
# progbar.grid(row=rows.index('progbar'),column=0, pady=10)

## Progress bar - normal tkinter

def flash(type):
	if type == 'wrong':
		for loop in range(10):
			progbar.configure(progress_color='#ff0000')
			time.sleep(0.1)
			progbar.configure(progress_color=colourmain)
			time.sleep(0.1)
	if type == 'pointless':
		for loop in range(10):
			progbar.configure(fg_color='#00ff00')
			time.sleep(0.1)
			progbar.configure(fg_color='#000')
			time.sleep(0.1)

global progvar
progvar = IntVar()
progvar.set(1)
progbar = CTkProgressBar(rightframe, orientation='vertical', width=50, height=500, corner_radius=0, mode='determinate', fg_color='black', progress_color=colourmain, variable=progvar)
progbar.grid(row=rows.index('progbar'),column=0, pady=10)

## Run button
run_button = CTkButton(rightframe, text='RUN', command=lambda:threading.Thread(target=lambda: run(pointless_score)).start(), font=(custom_font, 15), fg_color=colourmain, hover_color=colourdark, text_color='black', state='normal', text_color_disabled=colourdark)
run_button.grid(row=rows.index('run'),column=0)


# https://www.geeksforgeeks.org/python-focus_set-and-focus_get-method/
# master.bind_all('<Button-1>', lambda event: focus(event))

master.mainloop()