""" AutoClicker&Macro, a windows autoclicker&macro
 All source files in this repository are licensed under the
 GNU General Public License v2.0.
 Dependencies are licensed by their own.

 https://github.com/Assassin654/AutoClicker
 """

# this is a early build. to get latest features/performance get the latest from the releases tab
import autoit
import time
import sys
from sys import exit
import os
import tkinter
from tkinter import *
import customtkinter
import keyboard
import numpy
import threading
import requests
import tempfile

root = customtkinter.CTk()
title= 'Paul\'s Auto Clicker & Macro'
root.title(title)
root.geometry('800x500')
root.attributes('-topmost',True)
root.resizable(False,False)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

showPosition = True
version = '0.0.0'
menuFrame = customtkinter.CTkFrame(master=root, width=585, height=400)
menuFrame.place(x=210, y=5)


###### auto clicker frame
clicking = False
delay = 0
def check():
    global delay
    global repeats
    global MouseoffsetX
    global MouseoffsetY
    global Clickoffset
    global MousepositionX
    global MousepositionY
    try:
        mil = int(mil_interval.get())
    except:
        if (mil_interval.get()).strip(' ') == '':
            mil = 0
        else:
            showWarning.configure(text='Warning: Invalid input in milliseconds', text_color='red')
            return False
    try:
        sec = int(sec_interval.get())
    except:
        if (sec_interval.get()).strip(' ') == '':
            sec = 0
        else:
            showWarning.configure(text='Warning: Invalid input in seconds', text_color='red')
            return False
    try:
        min = int(min_interval.get())
    except:
        if (min_interval.get()).strip(' ') == '':
            min = 0
        else:
            showWarning.configure(text='Warning: Invalid input in minutes', text_color='red')
            return False
    try:
        hour = int(hour_interval.get())
    except:
        if (hour_interval.get()).strip(' ') == '':
            hour = 0
        else:
            showWarning.configure(text='Warning: Invalid input in hour', text_color='red')
            return False
    try:
        Clickoffset = int(interval_entry.get())
    except:
        if (interval_entry.get()).strip(' ') == '':
            Clickoffset = 50
        else:
            showWarning.configure(text='Warning: Invalid interval offset', text_color='red')
            return False
    try:
        MouseoffsetX = int(mouseX_entry.get())
        MouseoffsetY = int(mouseY_entry.get())
    except:
        if (mouseX_entry.get()).strip(' ') == '' and (mouseY_entry.get()).strip(' ') == '':
            MouseoffsetX = 25
            MouseoffsetY = 25
        else:
            showWarning.configure(text='Warning: Invalid mouse offset', text_color='red')
            return False
    try:
        MousepositionX = int(mouseX_position.get())
        MousepositionY = int(mouseY_position.get())
    except:
        if (mouseX_position.get()).strip(' ') == '' and (mouseY_position.get()).strip(' ') == '':
            MousepositionX = 0
            MousepositionY = 0
        else:
            showWarning.configure(text='Warning: Invalid cursor position', text_color='red')
            return False
    try:
        repeats = int(repeatTimes.get())
    except:
        if (repeatTimes.get()).strip(' ') == '':
            repeats = 1
        else:
            showWarning.configure(text='Warning: Invalid repeat option', text_color='red')
            return False
    delay = mil+(sec*1000)+(min*60000)+(hour*3600000)
    showWarning.configure(text='Warning: None', text_color='white')
        

def toggle_clicker():
    global clicking
    global clickingType
    global repeating
    global offsetInterval
    global offsetMouse
    global customPosition
    global times
    global pressButton
    if check() == False:
        clicking = False
        autoStart.configure(state='enabled')
        autoStop.configure(state='disabled') 
        showStatus.configure(text='Status: Stopped')
        return
    
    pressButton = mouseButton_entry.get()
    if mouseType_entry.get() == 'Double':
        clickingType = 2
    else:
        clickingType = 1 
        
    if repeat_var.get() == 1:
        repeating = True
        times = 0
    else:
        repeating = False
        
    if interval_switch.get() == True:
        offsetInterval = True
    else:
        offsetInterval = False
        
    if mouse_switch.get() == True:
        offsetMouse = True
    else:
        offsetMouse = False
    
    if position_var.get() == 1:
        customPosition = True
    else:
        customPosition = False
    
    clicking = not clicking
    if clicking == True:
        autoStart.configure(state='disabled')
        autoStop.configure(state='enabled')
        showStatus.configure(text='Status: Clicking')
    else:
        autoStart.configure(state='enabled')
        autoStop.configure(state='disabled') 
        showStatus.configure(text='Status: Stopped')


keyboard.add_hotkey('F6', lambda:toggle_clicker())

clickFrame = customtkinter.CTkFrame(master=root, width=585, height=400)
clickFrame.place(x=210, y=5)

clickInterval = customtkinter.CTkFrame(master=clickFrame, width=570, height=80)
clickInterval.place(x=5, y=5)
customtkinter.CTkLabel(master=clickInterval, text='Click Interval:').place(x=5,y=1)
customtkinter.CTkLabel(master=clickInterval,text='Milliseconds:').place(x=5,y=35)
mil_interval = customtkinter.CTkEntry(master=clickInterval, placeholder_text='0', width=70)
mil_interval.insert(0,'100')
mil_interval.place(x=90,y=35)
customtkinter.CTkLabel(master=clickInterval,text='Seconds:').place(x=170,y=35)
sec_interval = customtkinter.CTkEntry(master=clickInterval, placeholder_text='0', width=70)
sec_interval.place(x=230,y=35)
customtkinter.CTkLabel(master=clickInterval,text='Minutes:').place(x=310,y=35)
min_interval = customtkinter.CTkEntry(master=clickInterval, placeholder_text='0', width=70)
min_interval.place(x=370,y=35)
customtkinter.CTkLabel(master=clickInterval,text='Hours:').place(x=450,y=35)
hour_interval = customtkinter.CTkEntry(master=clickInterval, placeholder_text='0', width=70)
hour_interval.place(x=495,y=35)

interval_offset = customtkinter.CTkFrame(master=clickFrame, width=270, height=80)
interval_offset.place(x=5,y=95)
delay_interval = customtkinter.BooleanVar(value=False)
interval_switch = customtkinter.CTkSwitch(master=interval_offset, text='Interval offset:', variable=delay_interval, offvalue=False, onvalue=True)
interval_switch.place(x=5, y=1)
customtkinter.CTkLabel(master=interval_offset, text='Milliseconds:').place(x=5,y=35)
interval_entry = customtkinter.CTkEntry(master=interval_offset, placeholder_text='50', width=70)
interval_entry.place(x=90,y=35)

mouse_offset = customtkinter.CTkFrame(master=clickFrame, width=290, height=80)
mouse_offset.place(x=285,y=95)
mouse_switch = customtkinter.CTkSwitch(master=mouse_offset, text='Mouse offset:')
mouse_switch.place(x=5, y=1)
customtkinter.CTkLabel(master=mouse_offset, text='X:').place(x=5,y=35)
mouseX_entry = customtkinter.CTkEntry(master=mouse_offset, placeholder_text='25', width=45)
mouseX_entry.place(x=25,y=35)
customtkinter.CTkLabel(master=mouse_offset, text='Y:').place(x=75,y=35)
mouseY_entry = customtkinter.CTkEntry(master=mouse_offset, placeholder_text='25', width=45)
mouseY_entry.place(x=95,y=35)

clickOption = customtkinter.CTkFrame(master=clickFrame, width=570, height=80)
clickOption.place(x=5,y=185)
customtkinter.CTkLabel(master=clickOption,text='Click Options:').place(x=5,y=1)
customtkinter.CTkLabel(master=clickOption,text='Mouse Button:').place(x=5,y=35)
mouseButton_entry = customtkinter.CTkOptionMenu(master=clickOption, values=['Left','Right','Middle'], width=100)
mouseButton_entry.place(x=95,y=35)
customtkinter.CTkLabel(master=clickOption,text='Click Type:').place(x=205,y=35)
mouseType_entry = customtkinter.CTkOptionMenu(master=clickOption, values=['Single','Double'], width=100)
mouseType_entry.place(x=275,y=35)

cursorPosition = customtkinter.CTkFrame(master=clickFrame, width=250,height=80)
cursorPosition.place(x=5,y=275)
position_var = tkinter.IntVar(value=0)
customtkinter.CTkLabel(master=cursorPosition,text='Cursor Position:').place(x=5,y=1)
current = customtkinter.CTkRadioButton(master=cursorPosition, text='Current', variable=position_var, value=0, radiobutton_height=10,radiobutton_width=10)
current.place(x=5,y=25)
custom = customtkinter.CTkRadioButton(master=cursorPosition, text='Custom', variable=position_var, value=1, radiobutton_height=10,radiobutton_width=10)
custom.place(x=5,y=45)
customtkinter.CTkLabel(master=cursorPosition, text='X:').place(x=75,y=43)
mouseX_position = customtkinter.CTkEntry(master=cursorPosition, placeholder_text='0', width=45)
mouseX_position.place(x=95,y=43)
customtkinter.CTkLabel(master=cursorPosition, text='Y:').place(x=150,y=43)
mouseY_position = customtkinter.CTkEntry(master=cursorPosition, placeholder_text='0', width=45)
mouseY_position.place(x=170,y=43)

autoController = customtkinter.CTkFrame(master=clickFrame, width=310, height=80)
autoController.place(x=265,y=275)
customtkinter.CTkLabel(master=autoController, text='Repeat Options:').place(x=5,y=1)
repeat_var = tkinter.IntVar(value=0)
controllerToggle = customtkinter.CTkRadioButton(master=autoController, text='Toggle', variable=repeat_var, value=0)
controllerToggle.place(x=5,y=35)
controllerRepeat = customtkinter.CTkRadioButton(master=autoController, text='Repeat', variable=repeat_var, value=1)
controllerRepeat.place(x=160,y=35)
repeatTimes = customtkinter.CTkEntry(master=autoController, placeholder_text='1', width=50)
repeatTimes.place(x=235, y=33)


autoStart = customtkinter.CTkButton(master=clickFrame, text=f'Start (F6)', command=toggle_clicker)
autoStart.place(x=146,y=365)
autoStop = customtkinter.CTkButton(master=clickFrame, text=f'Stop (F6)', state='disabled', command=toggle_clicker)
autoStop.place(x=293,y=365)

###### macro frame
macroFrame = customtkinter.CTkFrame(master=root, width=585, height=400)

lb_macro = customtkinter.CTkLabel(master=macroFrame,text='Macro\'s')
lb_macro.place(x=1,y=1)

###### settings frame
settingFrame = customtkinter.CTkFrame(master=root, width=585, height=400)

lb_settings = customtkinter.CTkLabel(master=settingFrame,text='Settings')
lb_settings.place(x=1,y=1)


######home frame
def getAppearance(newAppearance):
    customtkinter.set_appearance_mode(newAppearance)
def getFrame(swap):
    if swap == 'clicker':
        clickFrame.place(x=210, y=5)
        tabClicker.configure(state='disabled')
        lb_home.configure(text='Auto Clicker')
    else:
        clickFrame.place_forget()
        tabClicker.configure(state='enabled')
    if swap == 'macro':
        tabMacro.configure(state='disabled')
        macroFrame.place(x=210, y=5)
        lb_home.configure(text='Macro')
    else:
        macroFrame.place_forget()
        tabMacro.configure(state='enabled')
    if swap == 'setting':
        settingFrame.place(x=210, y=5)
        tabSetting.configure(state='disabled')
        lb_home.configure(text='Settings')
    else:
        settingFrame.place_forget()
        tabSetting.configure(state='enabled')
def getClicker():
    getFrame('clicker')
def getMacro():
    getFrame('macro')
def getSetting():
    getFrame('setting')

homeFrame = customtkinter.CTkFrame(master=root, width=200,height=490)
homeFrame.place(x=5, y=5)
lb_home = customtkinter.CTkLabel(master=homeFrame, text='Auto Clicker', font=('whitney',20),width=125, height=30)
lb_home.place(x=37.5,y=25)
tabClicker = customtkinter.CTkButton(master=homeFrame, text='Auto Clicker', width=125, height=30, command=getClicker, state='disabled')
tabClicker.place(x=37.5,y=80)
tabMacro = customtkinter.CTkButton(master=homeFrame, text='Macro', width=125, height=30, command=getMacro)
tabMacro.place(x=37.5,y=135)
tabSetting = customtkinter.CTkButton(master=homeFrame, text='Settings', width=125, height=30, command=getSetting)
tabSetting.place(x=37.5,y=190)
lb_appearanceMode = customtkinter.CTkLabel(master=homeFrame, text='Appearance:', width=125, height=30)
lb_appearanceMode.place(x=37.5,y=400)
appearanceMenu = customtkinter.CTkOptionMenu(master=homeFrame, values=['System','Dark','Light'], command=getAppearance, width=125, height=30)
appearanceMenu.place(x=37.5,y=430)

##### main loop
def mainLoop():
    mousePos = autoit.mouse_get_pos()
    showMouse.configure(text=f'Mouse Position: {mousePos}')
    root.after(1,mainLoop)    
showMouse = customtkinter.CTkLabel(master=root)
showMouse.place(x=610, y=465)
showStatus = customtkinter.CTkLabel(master=root, text='Status: Stopped', font=('whitney',16))
showStatus.place(x=610, y=420)
showWarning = customtkinter.CTkLabel(master=root, text='Warnings: None')
showWarning.place(x=210, y=420)
if showPosition:
    mainLoop()


def autoclicker():
    global times
    while True:
        if clicking:
            if repeating == True:
                if times >= repeats:
                    toggle_clicker()
                else:
                    times = times + 1
            if customPosition == True:
                autoit.mouse_move(x=MousepositionX,y=MousepositionY, speed=0)
            if offsetMouse == True:
                xoff = numpy.random.uniform(-MouseoffsetX,MouseoffsetX)
                yoff = numpy.random.uniform(-MouseoffsetY,MouseoffsetY)
                pos = autoit.mouse_get_pos()
                xoff = int(xoff+pos[0])
                yoff = int(yoff+pos[1])
                autoit.mouse_move(x=xoff,y=yoff, speed=0)
            if offsetInterval == True:
                offset = numpy.random.uniform(-Clickoffset,Clickoffset)
            autoit.mouse_click(button=pressButton, clicks=clickingType)
            time.sleep((delay if offsetInterval == False else numpy.absolute(delay+offset))*.001)
        time.sleep(0.00000000000000000001)


########### updater
def defaultversion():
    updateButton.configure(text=f'Version: {version}',text_color='white')
def downloader():
    download = requests.get(f'https://github.com/Assassin654/AutoClicker/releases/download/{updateVersion}/version.exe', allow_redirects=True)
    os.chdir(tempfile.gettempdir())
    open('version.exe', 'wb').write(download.content)
    os.startfile('version.exe')
    sys.exit()
    
def updater():
    try:
        update = requests.get('https://api.github.com/repos/Assassin654/AutoClicker/releases/latest')
        updateVersion = (update.json()["name"])
    
        if updateVersion != version:
            updateButton.configure(text_color='yellow')
            showWarning.configure(text='Warnings: None')
            window = customtkinter.CTkToplevel()
            window.title('Updater')
            window.geometry('320x100')
            window.attributes('-topmost',True)
            window.grab_set()
            window.resizable(False,False)
            customtkinter.CTkLabel(master=window, text=f'Latest version: {updateVersion}\tCurrent Version: {version}').pack(side='top',pady=10)
            cancelButton = customtkinter.CTkButton(master=window, text='Cancel', command=window.destroy)
            cancelButton.place(x=5,y=50)
            downloadButton = customtkinter.CTkButton(master=window, text='Update', command=downloader)
            downloadButton.place(x=175,y=50)
        else:
            updateButton.configure(text='Version: Latest!', text_color='green')
            showWarning.configure(text='Warnings: None', text_color='white')
            root.after(2000, defaultversion)
    except:
        showWarning.configure(text='Warnings: API ratelimit on updates', text_color='yellow')
        
updateButton = customtkinter.CTkButton(master=root, text=f'Version: {version}',bg_color='transparent',fg_color='transparent', hover_color='grey', border_spacing = 0, width=0, command=updater)
updateButton.place(x=205, y=465)
try:
    update = requests.get('https://api.github.com/repos/Assassin654/AutoClicker/releases/latest')
    updateVersion = (update.json()["name"])
    if updateVersion != version:
        updateButton.configure(text_color='yellow')
except:
    showWarning.configure(text='Warnings: Could\'t check for latest version')

clickthread = threading.Thread(target=autoclicker)
clickthread.start()

root.mainloop()
