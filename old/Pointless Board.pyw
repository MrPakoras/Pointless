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
		mixer.music.play()

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


	run_button.configure(state='normal')

### GUI

## Importing font
appdatalocal = os.getenv('LOCALAPPDATA')
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file('./assets/Bangers-Regular_0.ttf')
custom_font = ('Bangers',30)
custom_font_title = ('Bangers',60)


master = CTk()
master.geometry("1000x800")
set_default_color_theme('green')
rows = ['title', 'setpoints', 'points', 'progbar', 'run'] # Index of rows so I dont have to manually update each .grid

mainframe = CTkFrame(master, width=1000, height=800) # Split window in half for image on left side
mainframe.grid(row=0, column=0)

leftframe = CTkScrollableFrame(mainframe, width=600, height=600) # Left side - for image
leftframe.grid(row=1, column=0, padx=0, ipadx=0)

rightframe = CTkFrame(mainframe, height=600) # Right side - for GUI elements
rightframe.grid(row=1, column=1)


colourmain = '#8d73ff'
colourdark = '#5a49a4'


## Title
title_label = CTkLabel(mainframe, text=' Pointless ', font=custom_font_title, text_color=colourmain)
title_label.grid(row=0, column=0)



## Left Frame

# Focus event on click
def focus(event):
	event.widget.focus_set()
	print(master.focus_get())

def focus_in(widget):
	widget.configure(border_color='#fff')

def focus_out(widget):
	widget.configure(border_color='#000')


players = [['Default', 0], ['P1', 0]]

for x in players:
	player_frame = CTkFrame(leftframe, width=600, height=200, border_width=5)
	player_frame.grid(row=players.index(x), column=0, pady=10, ipadx=10, ipady=10)
	player_frame.bind('<FocusIn>', lambda widget=player_frame: focus_in(widget))
	player_frame.bind('<FocusOut>', lambda widget=player_frame: focus_out(widget))

	player_name = CTkEntry(player_frame, width=550, height=20, font=custom_font, placeholder_text=x[0])
	player_name.grid(row=0, column=0)

	player_points_label = CTkLabel(player_frame, width=100, height=20, font=custom_font, text=x[1], padx=10)
	player_points_label.grid(row=1, column=0)


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

points_label = CTkLabel(rightframe, text=pointsvar.get(), font=custom_font_title, text_color=colourmain, padx=10)
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
run_button = CTkButton(rightframe, text='RUN', command=lambda:threading.Thread(target=lambda: run(pointless_score)).start(), fg_color=colourmain, hover_color=colourdark, text_color='black', state='normal', text_color_disabled=colourdark)
run_button.grid(row=rows.index('run'),column=0)


# https://www.geeksforgeeks.org/python-focus_set-and-focus_get-method/
master.bind_all('<Button-1>', lambda event: focus(event))

master.mainloop()