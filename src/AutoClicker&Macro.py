""" AutoClicker&Macro, a windows autoclicker&macro
 All source files in this repository are licensed under the
 GNU General Public License v2.0.
 Dependencies are licensed by their own.

 https://github.com/Assassin654/AutoClicker
 """

import pickle
import os
from subprocess import Popen, CREATE_NO_WINDOW
try:
    with open ('ACM.pkl', 'rb') as f:
        simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer = pickle.load(f)
except:
    simple = False
    themeColor = 'green'
    appearanceMode = 'System'
    clickerHotkey = 'F6'
    macroRecordHotkey = 'F7'
    macroStopHotkey = 'F8'
    macroPlayHotkey = 'F9'
    onTop = True
    showMousePosition = True
    superClicker = False
    mouseTimer = False
    with open('ACM.pkl', 'wb') as f:
        pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)

#pyinstaller  --icon=mouse.ico AutoClickerMacro.pyw
version = '1.2.4'

if simple:
    #Popen(['python','simplifiedClicker.pyw', str(version)])
    Popen(['simplifiedClicker.exe', str(version)])
    os._exit(os.EX_OK)
    #os._exit(0)

import autoit
import time
import tkinter
from tkinter import *
import customtkinter
import keyboard
import mouse
import threading
import requests
import random
import win32gui
import win32ui

if not os.path.exists("Macros"):
    os.mkdir('Macros')

cwd = os.getcwd()
pid = os.getpid()
#killSwitch = Popen(['python','ACM_failsafe.pyw', str(pid)])
killSwitch = Popen(['ACM_failsafe.exe', str(pid)])

root = customtkinter.CTk()
if superClicker:
    title = 'Paul\'s Auto Clicker & Macro - SuperMode'
else:
    title = 'Paul\'s Auto Clicker & Macro'

root.title(title)
root.geometry('800x500')
root.attributes('-topmost',onTop)
root.resizable(False,False)

customtkinter.set_appearance_mode(appearanceMode)
customtkinter.set_default_color_theme(themeColor)
root.iconbitmap('mouse.ico')

menuFrame = customtkinter.CTkFrame(master=root, width=585, height=400)
menuFrame.place(x=210, y=5)

###### auto clicker frame
clicking = False
recording = False
playing = False
saving = False
gettingPosition = False
delay = 0

def initiate_hotkeys():
    keyboard.hook_key(clickerHotkey, lambda e:toggle_clicker(str(e)))
    keyboard.hook_key(macroRecordHotkey, lambda e:checkMacro(str(e)))
    keyboard.hook_key(macroStopHotkey, lambda e:stopMacro(str(e)))
    keyboard.hook_key(macroPlayHotkey, lambda e:startMacro(str(e)))
    
initiate_hotkeys()

def check():
    global delay
    global repeats
    global MouseoffsetX
    global MouseoffsetY
    global Clickoffset
    global MousepositionX
    global MousepositionY
    global holding
    global restrictClicker
    global subWindow
    
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
    try:
        holding = float(holdDuration.get())
    except:
        if (holdDuration.get()).strip(' ') == '':
            holding = 0
        else:
            showWarning.configure(text='Warning: Invalid hold duration', text_color='red')
            return False
    if alternatingBox.get() == True and mouseButton_entry.get() == 'Middle':
        showWarning.configure(text='Warning: Can not use alternating with middle mouse button', text_color='red')
        return False
    if holding > 0 and  mouseType_entry.get() != 'Single':
        showWarning.configure(text=f'Warning: Can not {mouseType_entry.get()} click with holding', text_color='red')
        return False
    delay = mil+(sec*1000)+(min*60000)+(hour*3600000)
    if delay < 0:
        showWarning.configure(text='Warning: Delay can not be negative', text_color='red')
        return False
    try:
        (delay*.001)+(Clickoffset*.001)
    except:
        showWarning.configure(text='Warning: Delay is too large', text_color='red')
        return False
    if restrictingClicker and clicking == False:
        try:
            for key in windows:
                if key == windows_entry.get():
                    restrictClicker = {windows_entry.get():windows[key]}
                    break
                else:
                    restrictClicker = 0
            if restrictClicker == 0:
                raise
        except:
            showWarning.configure(text='Warning: Selected window no longer exists', text_color='red')
            return False
    if ghostClick_switch.get():
        if pressButton == 'Middle':
            showWarning.configure(text='Warning: Can not use middle mouse button with ghost click', text_color='red')
            return False
        updateWindows(None)
        if control_window == 0:
            showWarning.configure(text='Warning: Selected window no longer exists', text_color='red')
            return False
        if 'Any Window' in control_window:
            showWarning.configure(text='Warning: No window is selected', text_color='red')
            return False
        try:
            if clicking == False:
                subWindow = win32ui.CreateWindowFromHandle(list(control_window.values())[0])
        except:
            showWarning.configure(text='Warning: Can not use ghost click for selected window', text_color='red')
            return False
            
    showWarning.configure(text='Warning: None', text_color=('black', 'white'))     

def toggle_clicker(e):
    if 'down' not in e: return
    global clicking
    global clickingType
    global repeating
    global offsetInterval
    global offsetMouse
    global customPosition
    global times
    global pressButton
    global alternating
    global waiting
    global restrictingClicker
    global ghostClick
    
    if restrict_windows.get():
        restrictingClicker = True
        get_window_list()
    else:
        restrictingClicker = False
    
    if ghostClick_switch.get():
        ghostClick = True
        get_window_list()
    else:
        ghostClick = False
    
    pressButton = mouseButton_entry.get()
    
    if check() == False:
        clicking = False
        autoStart.configure(state='enabled')
        autoStop.configure(state='disabled') 
        showStatus.configure(text='Status: Stopped')
        return
    if recording:
        showWarning.configure(text='Warning: Can not use autoclicker while recording', text_color='red')
        return
    if saving:
        showWarning.configure(text='Warning: Can not use autoclicker while saving macro', text_color='red')
        return
    if gettingPosition:
        showWarning.configure(text='Warning: Can not use autoclicker while getting cursor position', text_color='red')
        return
    
    waiting = 0
    if mouseType_entry.get() == 'Double':
        clickingType = 2
    elif mouseType_entry.get() == 'Triple':
        clickingType = 3
    else:
        clickingType = 1 
        
    if repeat_var.get() == 1:
        repeating = True
        times = 0
    else:
        repeating = False
        
    if interval_switch.get():
        offsetInterval = True
    else:
        offsetInterval = False
        
    if mouse_switch.get():
        offsetMouse = True
    else:
        offsetMouse = False
    
    if position_var.get() == 1:
        customPosition = True
    else:
        customPosition = False
    
    if alternatingBox.get():
        alternating = True
    else:
        alternating = False
    
    clicking = not clicking
    if clicking:
        autoStart.configure(state='disabled')
        autoStop.configure(state='enabled')
        if playing:
            showStatus.configure(text='Status: Playing Macro &\nClicking')
        else:
            showStatus.configure(text='Status: Clicking')
    else:
        autoStart.configure(state='enabled')
        autoStop.configure(state='disabled')
        if playing:
            showStatus.configure(text='Status: Playing Macro')
        else:
            showStatus.configure(text='Status: Stopped')

def get_mouse_position():
    global gettingPosition
    if clicking:
        showWarning.configure(text='Warning: Can not get cursor position while clicking', text_color='red')
        return
    showWarning.configure(text='Warning: None', text_color=('black', 'white'))
    gettingPosition = True
    root.iconify()
    window = customtkinter.CTkToplevel()
    window.geometry("170x45")
    window.resizable(False,False)
    window.attributes('-topmost',True)
    window.overrideredirect(True)
    customtkinter.CTkLabel(master=window,text='Click to get mouse position').place(x=0,y=0)
    pos = customtkinter.CTkLabel(master=window,text=f'')
    pos.place(x=0,y=21)
    def move_window():
        global gettingPosition
        if ghostClick_switch.get():
            mousePos = f'Relative: ({rel_x},{rel_y})'
        else:
            mousePos = autoit.mouse_get_pos()
        x = window.winfo_pointerx()
        y = window.winfo_pointery() 
        pos.configure(text=f'{mousePos}')
        window.geometry(f"+{x+10}+{y+10}")
        if mouse.is_pressed(button='left'):
            if ghostClick_switch.get():
                x,y = rel_x,rel_y
            else:
                x,y = autoit.mouse_get_pos()
            mouseX_position.delete(0,END)
            mouseY_position.delete(0,END)
            mouseX_position.insert(0,f'{x}')
            mouseY_position.insert(0,f'{y}')
            window.destroy()
            gettingPosition = False
            root.state(newstate='normal')
        else:
            window.after(30, move_window)
    window.after(200,move_window)
    window.mainloop()

clickFrame = customtkinter.CTkFrame(master=root, width=585, height=400)
clickFrame.place(x=210, y=5)

clickInterval = customtkinter.CTkFrame(master=clickFrame, width=570, height=80)
clickInterval.place(x=5, y=5)
customtkinter.CTkLabel(master=clickInterval, text='Click Interval:').place(x=5,y=1)
customtkinter.CTkLabel(master=clickInterval,text='Milliseconds:').place(x=5,y=35)
mil_interval = customtkinter.CTkEntry(master=clickInterval, placeholder_text='0', width=70)
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
mouseType_entry = customtkinter.CTkOptionMenu(master=clickOption, values=['Single','Double','Triple'], width=100)
mouseType_entry.place(x=275,y=35)
customtkinter.CTkLabel(master=clickOption, text='Hold duration (s):').place(x=395,y=5)
holdDuration = customtkinter.CTkEntry(master=clickOption, placeholder_text='0', width=45)
holdDuration.place(x=505,y=5)
alternatingBox = customtkinter.CTkCheckBox(master=clickOption, text='Alternating', onvalue=True, offvalue=False)
alternatingBox.place(x=395, y=45)

cursorPosition = customtkinter.CTkFrame(master=clickFrame, width=250,height=80)
cursorPosition.place(x=5,y=275)
position_var = tkinter.IntVar(value=0)
customtkinter.CTkLabel(master=cursorPosition,text='Cursor Position:').place(x=5,y=1)
get_position = customtkinter.CTkButton(master=cursorPosition, text='Get',width=60,height=20, command=get_mouse_position)
get_position.place(x=120,y=4)
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
controllerRepeat.place(x=100,y=35)
repeatTimes = customtkinter.CTkEntry(master=autoController, placeholder_text='1', width=50)
repeatTimes.place(x=175, y=33)

autoStart = customtkinter.CTkButton(master=clickFrame, text=f'Start ({clickerHotkey})', command=lambda:toggle_clicker('down'))
autoStart.place(x=146,y=365)
autoStop = customtkinter.CTkButton(master=clickFrame, text=f'Stop ({clickerHotkey})', state='disabled', command=lambda:toggle_clicker('down'))
autoStop.place(x=293,y=365)

###### macro frame
def openFile(name):
    fileName = name
    macroContent.delete('0.0','end')
    try:
        with open (f'Macros/{fileName}.txt', 'r') as macroContents:
            macroContent.insert('0.0', macroContents.read())
        showWarning.configure(text=f'Warning: None', text_color=('black', 'white'))
    except(FileNotFoundError):
        showWarning.configure(text=f'Warning: There is no {fileName} file to open', text_color=('red'))
        
def saveFile():
    fileName = MacroFile.get()
    with open (f'Macros/{fileName}.txt', 'w') as macroContents:
        macroContents.write(macroContent.get('0.0','end'))
    files = os.listdir('Macros')
    files = [x.split('.')[0] for x in files]
    MacroFile.configure(values=files)
    
def deleteFile():
    fileName = MacroFile.get()
    try:
        os.remove(f'Macros/{fileName}.txt')
        files = os.listdir('Macros')
        files = [x.split('.')[0] for x in files]
        MacroFile.configure(values=files)
        macroContent.delete('0.0','end')
        with open (f'Macros/{files[0]}.txt', 'r') as macroContents:
            macroContent.insert('0.0', macroContents.read())
        showWarning.configure(text=f'Warning: None', text_color=('black', 'white'))
    except(FileNotFoundError):
        showWarning.configure(text=f'Warning: There is no {fileName} file to delete', text_color=('red'))

def on_mouse_event(event):
    events.append(event)

def on_keyboard_event(event):
    events.append((event, time.time()))

def checkMacro(e):
    if 'down' not in e: return
    global recording
    global doKeyboard
    global doMouse
    if clicking:
        showWarning.configure(text='Warning: Can not record macro while clicking', text_color='red')
        return
    if playing:
        return
    if saving:
        return
    if recording:
        return
    doKeyboard = keyboardMacro_switch.get()
    doMouse = MouseMacro_switch.get()
    if doKeyboard == False and doMouse == False:
        showWarning.configure(text='Warning: Both capture modes are disabled', text_color='red')
        return

    showWarning.configure(text='Warning: None', text_color=('black', 'white'))
    showStatus.configure(text='Status: Recording')
    MacroRecord.configure(state='disabled')
    MacroPlay.configure(state='disabled')
    MacroStop.configure(state='enabled')
    macroContent.configure(state='disabled')
    recording = True

def recordMacro():
    global events
    global saving
    global recording
    recordTime = 0
    while True:
        if recording:
            events = []

            if doMouse:
                mouse.hook(on_mouse_event)
            if doKeyboard:
                keyboard.hook(on_keyboard_event)

            while recording:
                if recording:
                    recordTime = 1
                    time.sleep(100*.001)
        elif recordTime == 1:
            if doMouse:
                mouse.unhook(on_mouse_event)
            if doKeyboard:
                keyboard.unhook(on_keyboard_event)
            with open("rawMacro.txt", "w") as f:
                events = tuple(events)
                for event in events:
                    f.write(f"{event}\n")
            recordTime = 0
            saving = True

        else:
            time.sleep(100*.001)
        time.sleep(0.00000000000000000001)

def saveMacro():
    global saving
    global recording
    while True:
        if saving:
            events = []
            lastTime = 0
            lastCheck = ['','']
            with open("rawMacro.txt", "r") as f:
                f = tuple(f.readlines())
            for line in f:
                if line.startswith('(KeyboardEvent') and not 'Unknown' in line:
                    line = line[1:]
                    line = line[:-2]
                    line = line.strip().split()
                    
                    if len(line) == 4:
                        if not lastTime == 0:
                            macroDelay = round(float(line[3])-float(lastTime),3)
                            lastTime = line[3]
                            events.append((f'Delay {macroDelay}'))
                        else:
                            lastTime = line[3]
                        macroEvent = line[0]+' '+line[1]+' '+line[2].replace(',','')                    
                    else:
                        keyCheck = line[0].split('(')[1]
                        if clickerHotkey.lower() in keyCheck or macroPlayHotkey.lower() in keyCheck or macroStopHotkey.lower() in keyCheck or macroRecordHotkey.lower() in keyCheck:
                            continue
                        if not lastTime == 0:
                            macroDelay = round(float(line[2])-float(lastTime),3)
                            lastTime = line[2]
                            events.append((f'Delay {macroDelay}'))
                        else:
                            lastTime = line[2]
                        macroEvent = line[0]+' '+line[1].replace(',','')
                    events.append(macroEvent)
                elif line.startswith('MoveEvent'):
                    line = line[:-2]
                    line = line.strip().split()
                    
                    macroEvent = line[0].replace('(',' ').replace(',','')+' '+line[1].replace(',','')
                    macroCheck = macroEvent.strip().split()
                    if macroCheck[1] != lastCheck[0] or macroCheck[2] != lastCheck[1]:
                        eventTime = line[2].replace('time=','') 
                        if not lastTime == 0:
                            macroDelay = round(float(eventTime)-float(lastTime),3)
                            lastTime = eventTime
                            events.append((f'Delay {macroDelay}'))
                        else:
                            lastTime = eventTime
                        lastCheck.clear()
                        lastCheck.append(macroCheck[1])
                        lastCheck.append(macroCheck[2])
                        lastTime = eventTime
                        events.append(macroEvent)
                    else:
                        lastCheck.clear()
                        lastCheck.append(macroCheck[1])
                        lastCheck.append(macroCheck[2])
                elif line.startswith('ButtonEvent'):
                    line = line[:-2]
                    line = line.strip().split()
                    
                    eventTime = line[2].replace('time=','')
                    if not lastTime == 0:
                        macroDelay = round(float(eventTime)-float(lastTime),3)
                        lastTime = eventTime
                        events.append((f'Delay {macroDelay}'))
                    else:
                        lastTime = eventTime
                        
                    if 'double' in line[0]:
                        line[0] = line[0].replace('double','down')
                        
                    macroEvent = line[0].replace('event_type','type')+' '+line[1]
                    events.append(macroEvent.replace('(',' ').replace(',','').replace('\'',''))
                elif line.startswith('WheelEvent'):
                    line = line[:-2]
                    line = line.strip().split()
                                
                    eventTime = line[1].replace('time=','')
                    if not lastTime == 0:
                        macroDelay = round(float(eventTime)-float(lastTime),3)
                        lastTime = eventTime
                        events.append((f'Delay {macroDelay}'))
                    else:
                        lastTime = eventTime 
                    
                    macroEvent = line[0].replace('(',' ').replace(',','')
                    events.append(macroEvent.split('.')[0])
                else:
                    pass
            events = tuple(events)
            with open("Macros/lastMacro.txt", "w") as f:
                for event in events:
                    f.write(f"{event}\n")
            macroContent.configure(state='normal')
            macroContent.delete('0.0','end')
            with open (f'Macros/lastMacro.txt', 'r') as macroContents:
                macroContent.insert('0.0', macroContents.read())
            files = os.listdir('Macros')
            files = [x.split('.')[0] for x in files]
            MacroFile.configure(values=files)
            showStatus.configure(text='Status: Stopped')
            showWarning.configure(text='Warning: None', text_color=('black', 'white'))
            MacroRecord.configure(state='enabled')
            MacroPlay.configure(state='enabled')
            MacroStop.configure(text=f'Stop ({macroStopHotkey})',state='disabled')
            saving = False
        else:
            time.sleep(100*.001)
        time.sleep(0.00000000000000000001)
        
def stopMacro(e):
    if 'down' not in e: return
    global recording
    global playing
    if recording:
        MacroStop.configure(text='Stopping',state='disabled')
        showStatus.configure(text='Status: Saving Macro')
        showWarning.configure(text='Warning: Large recordings can take a moment to save', text_color=('#F4C430','yellow'))
        recording = False

        
    else:
        if clicking:
            showStatus.configure(text='Status: Clicking')
        else:
            showStatus.configure(text='Status: Stopped')
        playing = False
        MacroRecord.configure(state='enabled')
        MacroPlay.configure(state='enabled')
        MacroStop.configure(state='disabled')
        macroContent.configure(state='normal')

def startMacro(e):
    if 'down' not in e: return
    global playing
    global repeatMacro
    global macroRepeatOption
    global macroTimes
    global macroDelayOffset
    global macroOverrideDelay
    global macroOffsetDelay
    global macroOverride
    global macroWaiting
    global restrictMacro
    global restricingMacro
    global skip
    
    if restrict_windows.get() == True:
        restricingMacro = True
        get_window_list()
        try:
            for key in windows:
                if key == windows_entry.get():
                    restrictMacro = {windows_entry.get():windows[key]}
                    break
                else:
                    restrictMacro = 0
            if restrictMacro == 0:
                raise
        except:
            showWarning.configure(text='Warning: Selected window no longer exists', text_color='red')
            return False
    else:
        restricingMacro = False
    try:
        repeatMacro = int(macroRepeatTimes.get())
    except:
        if (macroRepeatTimes.get()).strip(' ') =='':
            repeatMacro = 1
        else:
            showWarning.configure(text='Warning: Invalid input for repeat option', text_color='red')
            return
    try:
        macroDelayOffset = float(macroDelayOffsetEntry.get())
    except:
        if (macroDelayOffsetEntry.get()).strip(' ') =='':
            macroDelayOffset = .05
        else:
            showWarning.configure(text='Warning: Invalid input for macro delay offset', text_color='red')
            return
    try:
        macroOverrideDelay = float(macroDelayOverrideEntry.get())
    except:
        if (macroDelayOverrideEntry.get()).strip(' ') =='':
            macroOverrideDelay = 0
        else:
            showWarning.configure(text='Warning: Invalid input for macro delay override', text_color='red')
            return
    
    if playing:
        return
    if saving:
        return
    if recording:
        return
    if repeatMacro_var.get() == 1:
        macroRepeatOption = True
    else:
        macroRepeatOption = False
    if overrideMacro_switch.get() == True:
        macroOverride = True
    else:
        macroOverride = False
    if DelayOffSetMacro_switch.get() == True:
        macroOffsetDelay = True
    else:
        macroOffsetDelay = False
        
    macroTimes = 0
    macroWaiting = 0
    skip = []
    showWarning.configure(text='Warning: None', text_color=('black', 'white'))
    if clicking:
        showStatus.configure(text='Status: Playing Macro &\nClicking')
    else:
        showStatus.configure(text='Status: Playing Macro')
    MacroRecord.configure(state='disabled')
    MacroPlay.configure(state='disabled')
    MacroStop.configure(state='enabled')
    macroContent.configure(state='disabled')
    playing = True

def playMacro():
    global playing
    global macroTimes
    global macroRepeatOption
    global repeatMacro
    global macroDelayOffset
    global macroOverride
    global macroOffsetDelay
    global macroWaiting
    global skip
    while True:
        if playing:
            if macroRepeatOption:
                if macroTimes >= repeatMacro:
                    stopMacro('down')
            if macroTimes == 0:
                events = []
                macroText = macroContent.get('0.0','end').splitlines()
                for text in macroText:
                    events.append(text)
                events = tuple(events)
            
            for i, event in enumerate(events):
                if playing:
                    if restricingMacro:
                        if 'Any Window' not in restrictMacro:
                            hwnd = win32gui.GetForegroundWindow()
                            if hwnd not in restrictMacro.values():
                                while hwnd not in restrictMacro.values():
                                    hwnd = win32gui.GetForegroundWindow()
                                    time.sleep(1*.001)
                    try:
                        event = event.lower()
                        
                        if i in skip:
                            continue
                        elif event.startswith('*'):
                            event = event.replace('*','')
                            skip.append(i)
                    
                        if event.startswith('#'):
                            continue
                        elif event.startswith('delay'):
                            if macroOverride:
                                event = [0, macroOverrideDelay]
                            else:
                                event = event.strip().split()
                            if macroOffsetDelay:
                                offset = random.uniform(-macroDelayOffset,macroDelayOffset)
                            if float(event[1]) >= 1:
                                macroWaiting = time.monotonic()+(float(event[1]) if macroOffsetDelay == False else abs(float(event[1])+offset))
                                while playing:
                                    if time.monotonic() >= macroWaiting:
                                        break
                                    time.sleep(1*.001)
                            else:
                                time.sleep(float(event[1]) if macroOffsetDelay == False else abs(float(event[1])+offset))
                        elif event.startswith('keyboardevent'):
                            event = event.replace('(',' ',1)[:-1]
                            event = event.strip().split()
                            if len(event) == 4:
                                if event[3] == 'down':
                                    keyboard.press(f'{event[1]} {event[2]}')
                                elif event[3] == 'up':
                                    keyboard.release(f'{event[1]} {event[2]}')
                            else:
                                if event[1] == clickerHotkey.lower() or event[1] == macroPlayHotkey.lower() or event[1] == macroStopHotkey.lower() or event[1] == macroPlayHotkey.lower():
                                    continue
                                elif event[2] == 'down':
                                    keyboard.press(event[1])
                                elif event[2] == 'up':
                                    keyboard.release(event[1])
                        elif event.startswith('moveevent'):
                            event = event.replace('x=','').replace('y=','')
                            event = event.strip().split()
                            autoit.mouse_move(x=int(event[1]),y=int(event[2]),speed=0)
                        elif event.startswith('buttonevent'):
                            event = event.replace('type=','').replace('button=','')
                            event = event.strip().split()
                            if event[1] == 'down':
                                autoit.mouse_down(button=event[2])
                            elif event[1] == 'up':
                                autoit.mouse_up(button=event[2])
                        elif event.startswith('wheelevent'):
                            event = event.replace('delta=','')
                            event = event.strip().split()
                            if int(event[1]) < 0:
                                autoit.mouse_wheel(direction='down', clicks=int(event[1].replace('-','')))
                            elif int(event[1]) > 0:
                                autoit.mouse_wheel(direction='up', clicks=int(event[1]))
                        elif event.startswith('click'):
                            if 'at' in event:
                                event = event.replace('button=','').replace('x=','').replace('y=','').replace('speed=','')
                                event = event.strip().split()
                                autoit.mouse_click(button=event[1], x=int(event[3]),y=int(event[4]), speed=int(event[5]))
                            else:
                                event = event.replace('button=','')
                                event = event.strip().split()
                                autoit.mouse_click(button=event[1])
                        elif event.startswith('presskey'):
                            event = event.replace('(',' ',1)[:-1]
                            event = event.strip().split()
                            if event[1] == clickerHotkey.lower() or event[1] == macroPlayHotkey.lower() or event[1] == macroStopHotkey.lower() or event[1] == macroPlayHotkey.lower():
                                continue
                            keyboard.press_and_release(event[1])
                        elif event.startswith('drag'):
                            event = event.replace('button=','').replace('x=','').replace('y=','').replace('speed=','')
                            event = event.strip().split()
                            autoit.mouse_click_drag(button=event[1], speed=int(event[2]), x1=int(event[3]), y1=int(event[4]), x2=int(event[6]), y2=int(event[7]))
                        elif event.startswith('type'):
                            event = event.replace('speed=','')
                            write = event.split('(')[1][:-1]
                            event = event.strip().split()
                            keyboard.write(delay=float(event[1]), text=write)
                        elif event.startswith('move'):
                            event = event.replace('x=','').replace('y=','').replace('speed=','')
                            event = event.strip().split()
                            autoit.mouse_move(x=int(event[1]), y=int(event[2]), speed=int(event[3]))
                    except:
                        showWarning.configure(text=f'Warning: Error reading line {i+1}', text_color=('#F4C430','yellow'))
            macroTimes = macroTimes + 1
        else:
            time.sleep(100*.001)
        time.sleep(0.00000000000000000001)

macroFrame = customtkinter.CTkFrame(master=root, width=585, height=400)

macroOptions = customtkinter.CTkFrame(master=macroFrame, width=570, height=100)
macroOptions.place(x=5,y=5)
customtkinter.CTkLabel(master=macroOptions,text='Capture:').place(x=5,y=5)
keySwitches = customtkinter.BooleanVar(value=True)
mouseSwitches = customtkinter.BooleanVar(value=True)
keyboardMacro_switch = customtkinter.CTkSwitch(master=macroOptions, text='Keyboard Input', variable=keySwitches, offvalue=False, onvalue=True)
keyboardMacro_switch.place(x=5,y=30)
MouseMacro_switch = customtkinter.CTkSwitch(master=macroOptions, text='Mouse Input', variable=mouseSwitches, offvalue=False, onvalue=True)
MouseMacro_switch.place(x=5,y=55)

overrideMacro_var = customtkinter.BooleanVar(value=False)
macroDelayOffset_var = customtkinter.BooleanVar(value=False)
customtkinter.CTkLabel(master=macroOptions,text='Delay Options:').place(x=180,y=5)
overrideMacro_switch = customtkinter.CTkSwitch(master=macroOptions, text='Delay Override', variable=overrideMacro_var, offvalue=False, onvalue=True)
overrideMacro_switch.place(x=180,y=30)
macroDelayOverrideEntry = customtkinter.CTkEntry(master=macroOptions, placeholder_text='0', width=45, height=23)
macroDelayOverrideEntry.place(x=310, y=30)
DelayOffSetMacro_switch = customtkinter.CTkSwitch(master=macroOptions, text='Delay Offset', variable=macroDelayOffset_var, offvalue=False, onvalue=True)
DelayOffSetMacro_switch.place(x=180,y=55)
macroDelayOffsetEntry = customtkinter.CTkEntry(master=macroOptions, placeholder_text='.05', width=45, height=23)
macroDelayOffsetEntry.place(x=299, y=55)

customtkinter.CTkLabel(master=macroOptions,text='Repeat Options:').place(x=390,y=5)
repeatMacro_var = tkinter.IntVar(value=0)
macroToggle = customtkinter.CTkRadioButton(master=macroOptions, text='Toggle', variable=repeatMacro_var, value=0)
macroToggle.place(x=390,y=33)
macroRepeat = customtkinter.CTkRadioButton(master=macroOptions, text='Repeat', variable=repeatMacro_var, value=1)
macroRepeat.place(x=390,y=66)
macroRepeatTimes = customtkinter.CTkEntry(master=macroOptions, placeholder_text='1', width=50)
macroRepeatTimes.place(x=465, y=63)

MacroRecord = customtkinter.CTkButton(master=macroFrame,text=f'Record ({macroRecordHotkey})', command=lambda:checkMacro('down'))
MacroRecord.place(x=72,y=365)
MacroStop = customtkinter.CTkButton(master=macroFrame,text=f'Stop ({macroStopHotkey})', state='disabled', command=lambda:stopMacro('down'))
MacroStop.place(x=222,y=365)
MacroPlay = customtkinter.CTkButton(master=macroFrame,text=f'Play ({macroPlayHotkey})', command=lambda:startMacro('down'))
MacroPlay.place(x=372,y=365)
macroContent = customtkinter.CTkTextbox(master=macroFrame, width=570,height=220)
macroContent.place(x=5,y=140)

files = os.listdir('Macros')
if not files:
    files.append('Macro 1')
    macroContent.insert('0.0','Macro Contents:\nView the help tab in settings for more information on how to create your own macros manually')
else:
    files = [x.split('.')[0] for x in files]
    with open (f'Macros/{files[0]}.txt', 'r') as macroContents:
        macroContent.insert('0.0', macroContents.read())

MacroFile = customtkinter.CTkComboBox(master=macroFrame, width=350, values=files, command=openFile)
MacroFile.place(x=5,y=109)
saveMacroFile = customtkinter.CTkButton(master=macroFrame,text='Save', width=95, command=saveFile)
saveMacroFile.place(x=365,y=109)
removeMacroFile = customtkinter.CTkButton(master=macroFrame,text='Delete', width=95, command=deleteFile, hover_color='dark red')
removeMacroFile.place(x=469,y=109)


###### settings frame
def applyTop():
    global onTop
    onTop = onTop_switch.get()
    root.attributes('-topmost',onTop)
    with open('ACM.pkl', 'wb') as f:
        pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)

def getTheme(newTheme):
    global themeColor
    showWarning.configure(text='Warning: Restart needed for changes to apply', text_color=('#F4C430','yellow'))
    themeColor = newTheme
    with open('ACM.pkl', 'wb') as f:
        pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)
        
def disable_event():
    pass

def clickerKeyChange():
    global clickerHotkey
    window = customtkinter.CTkToplevel()
    window.title('Update Autoclicker Key')
    window.geometry('250x100')
    window.iconphoto(False, PhotoImage(file='gear.png'))
    window.attributes('-topmost',True)
    window.grab_set()
    window.resizable(False,False)
    window.protocol("WM_DELETE_WINDOW", disable_event)
    customtkinter.CTkLabel(master=window, text='Press any key to set as new Hotkey', fg_color='grey', corner_radius=8).place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)
    keyboard.unhook_all()
    def key(waitkey):
        global clickerHotkey
        waitkey = waitkey.name
        if waitkey.upper() != macroRecordHotkey and waitkey.upper() != macroStopHotkey and waitkey.upper() != macroPlayHotkey:
            clickerHotkey = waitkey.upper()
            with open('ACM.pkl', 'wb') as f:
                pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)
            changeHotKey.configure(text=f'({clickerHotkey})')
            autoStart.configure(text=f'Start ({clickerHotkey})')
            autoStop.configure(text=f'Stop ({clickerHotkey})')
            showWarning.configure(text='Warning: None',text_color=('black', 'white'))
            window.destroy()
            keyboard.unhook_all()
            initiate_hotkeys()
        else:
            showWarning.configure(text='Warning: You can not bind this key to an existing hotkey',text_color='red')
    keyboard.on_press(key)
    window.mainloop()
    
def macroRecordKeyChange():
    global macroRecordHotkey
    window = customtkinter.CTkToplevel()
    window.title('Update Autoclicker Key')
    window.geometry('250x100')
    window.iconphoto(False, PhotoImage(file='gear.png'))
    window.attributes('-topmost',True)
    window.grab_set()
    window.resizable(False,False)
    window.protocol("WM_DELETE_WINDOW", disable_event)
    customtkinter.CTkLabel(master=window, text='Press any key to set as new Hotkey', fg_color='grey', corner_radius=8).place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)
    keyboard.unhook_all()
    def key(waitkey):
        global macroRecordHotkey
        waitkey = waitkey.name
        if waitkey.upper() != clickerHotkey and waitkey.upper() != macroStopHotkey and waitkey.upper() != macroPlayHotkey:
            macroRecordHotkey = waitkey.upper()
            with open('ACM.pkl', 'wb') as f:
                pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)
            changeRecordKey.configure(text=f'({macroRecordHotkey})')
            MacroRecord.configure(text=f'Record ({macroRecordHotkey})')
            showWarning.configure(text='Warning: None',text_color=('black', 'white'))
            window.destroy()
            keyboard.unhook_all()
            initiate_hotkeys()
        else:
            showWarning.configure(text='Warning: You can not bind this key to an existing hotkey',text_color='red')
    keyboard.on_press(key)
    window.mainloop()
    
def macroStopKeyChange():
    global macroStopHotkey
    window = customtkinter.CTkToplevel()
    window.title('Update Autoclicker Key')
    window.geometry('250x100')
    window.iconphoto(False, PhotoImage(file='gear.png'))
    window.attributes('-topmost',True)
    window.grab_set()
    window.resizable(False,False)
    window.protocol("WM_DELETE_WINDOW", disable_event)
    customtkinter.CTkLabel(master=window, text='Press any key to set as new Hotkey', fg_color='grey', corner_radius=8).place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)
    keyboard.unhook_all()
    def key(waitkey):
        global macroStopHotkey
        waitkey = waitkey.name
        if waitkey.upper() != macroRecordHotkey and waitkey.upper() != clickerHotkey and waitkey.upper() != macroPlayHotkey:
            macroStopHotkey = waitkey.upper()
            with open('ACM.pkl', 'wb') as f:
                pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)
            changeStopKey.configure(text=f'({macroStopHotkey})')
            MacroStop.configure(text=f'Stop ({macroStopHotkey})')
            showWarning.configure(text='Warning: None',text_color=('black', 'white'))
            window.destroy()
            keyboard.unhook_all()
            initiate_hotkeys()
        else:
            showWarning.configure(text='Warning: You can not bind this key to an existing hotkey',text_color='red')            
    keyboard.on_press(key)
    window.mainloop()
    
def macroPlayKeyChange():
    global macroPlayHotkey
    window = customtkinter.CTkToplevel()
    window.title('Update Autoclicker Key')
    window.geometry('250x100')
    window.iconphoto(False, PhotoImage(file='gear.png'))
    window.attributes('-topmost',True)
    window.grab_set()
    window.resizable(False,False)
    window.protocol("WM_DELETE_WINDOW", disable_event)
    customtkinter.CTkLabel(master=window, text='Press any key to set as new Hotkey', fg_color='grey', corner_radius=8).place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)
    keyboard.unhook_all()
    def key(waitkey):
        global macroPlayHotkey
        waitkey = waitkey.name
        if waitkey.upper() != macroRecordHotkey and waitkey.upper() != macroStopHotkey and waitkey.upper() != clickerHotkey:
            macroPlayHotkey = waitkey.upper()
            with open('ACM.pkl', 'wb') as f:
                pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)
            changePlayKey.configure(text=f'({macroPlayHotkey})')
            MacroPlay.configure(text=f'Play ({macroPlayHotkey})')
            showWarning.configure(text='Warning: None',text_color=('black', 'white'))
            window.destroy()
            keyboard.unhook_all()
            initiate_hotkeys()
        else:
            showWarning.configure(text='Warning: You can not bind this key to an existing hotkey',text_color='red')
    keyboard.on_press(key)
    window.mainloop()

def applyMouseSetting():
    global showMousePosition
    showMousePosition = mouseSetting_switch.get()
    applyMousePosition()
    if ghostClick_switch.get():
        applyControlClickPosition()
    with open('ACM.pkl', 'wb') as f:
        pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)

def disable_features_superclick():
    if restrict_windows.get():
        restrict_windows.toggle()
    restrict_windows.configure(state='disabled')
    if ghostClick_switch.get():
        ghostClick_switch.toggle()
    ghostClick_switch.configure(state='disabled')
    if repeat_var.get() == 1:
        repeat_var.set(0)
    controllerRepeat.configure(state='disabled')
    if interval_switch.get():
        interval_switch.toggle()
    interval_switch.configure(state='disabled')
    if mouse_switch.get():
        mouse_switch.toggle()
    mouse_switch.configure(state='disabled')
    if alternatingBox.get():
        alternatingBox.toggle()
    alternatingBox.configure(state='disabled')
    holdDuration.delete(0, END)
    holdDuration.configure(state='disabled')

def enable_features_superclicker():
    controllerRepeat.configure(state='normal')
    interval_switch.configure(state='enabled')
    mouse_switch.configure(state='enabled')
    restrict_windows.configure(state='enabled')
    ghostClick_switch.configure(state='enabled')
    alternatingBox.configure(state='normal')
    holdDuration.configure(state='normal')

def applySuperclicker():
    global superClicker
    global title
    superClicker = superClicker_switch.get()
    if superClicker:
        if not superclickerThread.is_alive():
            superclickerThread.start()
        disable_features_superclick()
        title = 'Paul\'s Auto Clicker & Macro - SuperMode'
        showWarning.configure(text='Warning: Super clicker enabled. Some options are limited', text_color='orange')
    else:
        enable_features_superclicker()
        title = 'Paul\'s Auto Clicker & Macro'
        showWarning.configure(text='Warning: None', text_color=('black', 'white'))
    with open('ACM.pkl', 'wb') as f:
        pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)

def applyMouseTimer():
    global mouseTimer
    mouseTimer = mouseTimer_switch.get()
    with open('ACM.pkl', 'wb') as f:
        pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)

def help():
    def re_enable():
        helpButton.configure(state='enabled')
        window.destroy()
    window = customtkinter.CTkToplevel()
    window.title('Autoclicker&Macro Help Window')
    window.geometry('800x400')
    window.iconphoto(False, PhotoImage(file='gear.png'))
    window.attributes('-topmost',True)
    helpButton.configure(state='disabled')
    window.resizable(False,False)
    helpTabs = customtkinter.CTkTabview(window)
    helpTabs.pack(expand=1, fill="both",pady=5,padx=5)
    window.protocol("WM_DELETE_WINDOW", re_enable)
    
    autoTab = helpTabs.add('Autoclicker')
    autoHelp = customtkinter.CTkTextbox(master=autoTab)
    autoHelp.pack(expand=1, fill="both")
    with open ('autotab.txt', 'r') as autotxt:
        autoHelp.insert('0.0', autotxt.read())
    autoHelp.configure(state='disabled')
        
    macroTab = helpTabs.add('Macro')
    macroHelp = customtkinter.CTkTextbox(master=macroTab)
    macroHelp.pack(expand=1, fill="both")
    with open ('macrotab.txt', 'r') as settingtxt:
        macroHelp.insert('0.0', settingtxt.read())
    macroHelp.configure(state='disabled')
    
    settingTab = helpTabs.add('Settings')
    settingHelp = customtkinter.CTkTextbox(master=settingTab)
    settingHelp.pack(expand=1, fill="both")
    with open ('settingtab.txt', 'r') as settingtxt:
        settingHelp.insert('0.0', settingtxt.read())
    settingHelp.configure(state='disabled')
    
    simpleTab = helpTabs.add('Simplify')
    simpleTab = customtkinter.CTkTextbox(master=simpleTab)
    simpleTab.pack(expand=1, fill="both")
    with open ('simpletab.txt', 'r') as settingtxt:
        simpleTab.insert('0.0', settingtxt.read())
    simpleTab.configure(state='disabled')
    
def openMacroFile():
    os.startfile(fr'{cwd}\Macros')

def defaultsharebutton():
    sharebutton.configure(text='Share')
def sharelink():
    import pyperclip
    pyperclip.copy(f'https://github.com/Assassin654/AutoClicker/releases/latest/download/AutoClickerMacroInstaller.exe')
    sharebutton.configure(text='Copied!')
    root.after(2000, defaultsharebutton)

def get_window_list():
    global windows
    try:
        def window_enum_handler(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                windows[win32gui.GetWindowText(hwnd)] = hwnd

        windows = {}
        win32gui.EnumWindows(window_enum_handler, windows)
        replace = {'':'Any Window'}
        for k, v in list(windows.items()):
            windows[replace.get(k, k)] = windows.pop(k)
        windows_entry.configure(values=windows)
        showWarning.configure(text='Warning: None', text_color=('black', 'white'))
    except:
        showWarning.configure(text='Warning: Error retrieving windows', text_color='Red')
    
def updateWindows(extra):
    global control_window
    control_window = 0
    if ghostClick_switch.get() and showMousePosition:
        for key in windows:
            if key == windows_entry.get():
                control_window = {windows_entry.get():windows[key]}
                break
            else:
                control_window = 0

def disable_features_ghostclicker():
    global position_var
    current.configure(state='disabled')
    position_var.set(value=1)
    mouseType_entry.configure(state='disabled')
    mouseType_entry.set('Single')
    alternatingBox.configure(state='disabled')
    holdDuration.delete(0, END)
    holdDuration.configure(state='disabled')
    
def enable_features_ghostclicker():
    current.configure(state='normal')
    mouseType_entry.configure(state='normal')
    alternatingBox.configure(state='normal')
    holdDuration.configure(state='normal')

def applyGhostClick():
    global title
    disable_features_ghostclicker()
    if ghostClick_switch.get():
        if restrict_windows.get():
            restrict_windows.toggle()
        if not mouseSetting_switch.get():
            mouseSetting_switch.toggle()
        updateWindows(None)
        applyControlClickPosition()
        title = 'Paul\'s Auto Clicker & Macro - GhostMode'
        showWarning.configure(text='Warning: Ghost click enabled. Some options are limited.\nPlease select a application. Note: does not work on all applications', text_color='orange')
    else:
        enable_features_ghostclicker()
        title = 'Paul\'s Auto Clicker & Macro'
        showWarning.configure(text='Warning: None', text_color=('black', 'white'))
    
def applyRestrictive():
    global title
    if restrict_windows.get():
        if ghostClick_switch.get():
            ghostClick_switch.toggle()
        title = 'Paul\'s Auto Clicker & Macro - Restricted'
        showWarning.configure(text='Warning: Restricting program to a window, please select a application', text_color='orange')
    else:
        title = 'Paul\'s Auto Clicker & Macro'
        showWarning.configure(text='Warning: None', text_color=('black', 'white'))

settingFrame = customtkinter.CTkFrame(master=root, width=585, height=400)

hotkeypage = customtkinter.CTkFrame(master=settingFrame, width=282, height=220)
hotkeypage.place(x=5,y=5)
customtkinter.CTkLabel(master=hotkeypage, text='Keybinds:').place(x=5,y=5)
customtkinter.CTkLabel(master=hotkeypage, text='Change Autoclicker Hotkey:').place(x=5,y=30)
changeHotKey = customtkinter.CTkButton(master=hotkeypage, text=f'({clickerHotkey})', width=20, command=clickerKeyChange)
changeHotKey.place(x=170,y=30)
customtkinter.CTkLabel(master=hotkeypage, text='Change Macro Record Hotkey:').place(x=5,y=65)
changeRecordKey = customtkinter.CTkButton(master=hotkeypage, text=f'({macroRecordHotkey})', width=20, command=macroRecordKeyChange)
changeRecordKey.place(x=185,y=65)
customtkinter.CTkLabel(master=hotkeypage, text='Change Macro Stop Hotkey:').place(x=5,y=100)
changeStopKey = customtkinter.CTkButton(master=hotkeypage, text=f'({macroStopHotkey})', width=20, command=macroStopKeyChange)
changeStopKey.place(x=170,y=100)
customtkinter.CTkLabel(master=hotkeypage, text='Change Macro Play Hotkey:').place(x=5,y=135)
changePlayKey = customtkinter.CTkButton(master=hotkeypage, text=f'({macroPlayHotkey})', width=20, command=macroPlayKeyChange)
changePlayKey.place(x=170,y=135)
customtkinter.CTkLabel(master=hotkeypage, text='Theme color: ').place(x=5,y=185)
themeMenu = customtkinter.CTkOptionMenu(master=hotkeypage, values=['green', 'blue', 'dark-blue'], variable=customtkinter.StringVar(value=themeColor), command=getTheme)
themeMenu.place(x=90,y=185)

generalsettings = customtkinter.CTkFrame(master=settingFrame, width=282, height=220)
generalsettings.place(x=295,y=5)
customtkinter.CTkLabel(master=generalsettings, text='General Settings:').place(x=5,y=5)
onTopSetting = customtkinter.BooleanVar(value=onTop)
onTop_switch = customtkinter.CTkSwitch(master=generalsettings, text='Always show window on top', variable=onTopSetting, offvalue=False, onvalue=True, command=applyTop)
onTop_switch.place(x=5,y=30)
mouseSetting = customtkinter.BooleanVar(value=showMousePosition)
mouseSetting_switch = customtkinter.CTkSwitch(master=generalsettings, text='Show mouse position', variable=mouseSetting, offvalue=False, onvalue=True, command=applyMouseSetting)
mouseSetting_switch.place(x=5,y=55)
superSetting = customtkinter.BooleanVar(value=superClicker)
superClicker_switch = customtkinter.CTkSwitch(master=generalsettings, text='Superclicker', variable=superSetting, offvalue=False, onvalue=True, command=applySuperclicker)
superClicker_switch.place(x=5,y=80)
mouseTimerSetting = customtkinter.BooleanVar(value=mouseTimer)
mouseTimer_switch = customtkinter.CTkSwitch(master=generalsettings, text='Show click delay timer', variable=mouseTimerSetting, offvalue=False, onvalue=True, command=applyMouseTimer)
mouseTimer_switch.place(x=5,y=105)

ghostClickSetting = customtkinter.BooleanVar(value=False)
ghostClick_switch = customtkinter.CTkSwitch(master=generalsettings, text='Ghost click', variable=ghostClickSetting, offvalue=False, onvalue=True, command=applyGhostClick)
ghostClick_switch.place(x=5,y=140)
restrict_setting = customtkinter.BooleanVar(value=False)
restrict_windows = customtkinter.CTkSwitch(master=generalsettings, text='Restrict to a window:', variable=restrict_setting, offvalue=False, onvalue=True, command=applyRestrictive)
restrict_windows.place(x=5,y=164)
refresh_windows = customtkinter.CTkButton(master=generalsettings, text='Refresh', command=get_window_list, height=10, width=65, corner_radius=100)
refresh_windows.place(x=200, y=164)
windows_entry = customtkinter.CTkOptionMenu(master=generalsettings, values=['Any Window'], width=280,dynamic_resizing=False, command=updateWindows)  
windows_entry.place(x=1,y=188)

helpButton = customtkinter.CTkButton(master=settingFrame,text='Help', width=80, command=help)
helpButton.place(x=20,y=235)
sharebutton = customtkinter.CTkButton(master=settingFrame, text='Share', width=90, height=30, command=sharelink)
sharebutton.place(x=160,y=235)
macroLocationButton = customtkinter.CTkButton(master=settingFrame,text='Open Macro Files', width=80, command=openMacroFile)
macroLocationButton.place(x=310,y=235)

changelog = customtkinter.CTkTextbox(master=settingFrame, width=570, height=120)
changelog.place(x=5,y=275)
with open ('changelog.txt', 'r') as changelogtxt:
    changelog.insert('0.0', changelogtxt.read())
changelog.configure(state='disabled')

######home frame
def getAppearance(newAppearance):
    global appearanceMode
    customtkinter.set_appearance_mode(newAppearance)
    appearanceMode = newAppearance
    with open('ACM.pkl', 'wb') as f:
        pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)

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

def simplify_toggle():
    if simplify_switch.get() == False:
        return
    global simple
    simple = simplify_switch.get()
    with open('ACM.pkl', 'wb') as f:
        pickle.dump([simple, themeColor, appearanceMode, clickerHotkey, macroRecordHotkey, macroStopHotkey, macroPlayHotkey, onTop, showMousePosition, superClicker, mouseTimer], f)
    #Popen(['python','simplifiedClicker.pyw', str(version)])
    Popen(['simplifiedClicker.exe', str(version)])
    root.destroy()

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
customtkinter.CTkLabel(master=homeFrame,text='CTRL+SHIFT+K \nTo kill the application').place(x=37.5,y=300)
lb_appearanceMode = customtkinter.CTkLabel(master=homeFrame, text='Appearance:', width=125, height=30)
lb_appearanceMode.place(x=37.5,y=400)
appearanceMenu = customtkinter.CTkOptionMenu(master=homeFrame, values=['System','Dark','Light'], command=getAppearance, width=125, height=30, variable=customtkinter.StringVar(value=appearanceMode))
appearanceMenu.place(x=37.5,y=430)
simplify_var = customtkinter.BooleanVar(value=simple)
simplify_switch = customtkinter.CTkSwitch(master=homeFrame, text='Simplified', variable=simplify_var, offvalue=False, onvalue=True, command=simplify_toggle)
simplify_switch.place(x=50.5,y=463)

##### mouse position loop
def applyMousePosition():
    if showMousePosition:
        mousePos = autoit.mouse_get_pos()
        showMouse.configure(text=f'Mouse Position: {mousePos}')
        root.after(30,applyMousePosition)  
    else:
        showMouse.configure(text='')

def applyControlClickPosition():
    global rel_x,rel_y
    rel_x, rel_y= 0, 0
    if ghostClick_switch.get() and showMousePosition:
        try:
            if control_window == 0:
                raise 
            elif 'Any Window' in control_window:
                raise
            rect = win32gui.GetWindowRect(list(control_window.values())[0])
            windowCoord_x = rect[0]
            windowCoord_y = rect[1]
            w = rect[2] - windowCoord_x
            h = rect[3] - windowCoord_y
            x, y = autoit.mouse_get_pos()
            rel_x = x - windowCoord_x
            rel_y = y - windowCoord_y
            if rel_x < 0 or rel_x > w:
                showControl.configure(text='Relative Position: Not inside the window')
            elif rel_y < 0 or rel_y > h:
                showControl.configure(text='Relative Position: Not inside the window')
            else:
                showControl.configure(text=f'Relative Position: ({rel_x},{rel_y})')
            root.after(30,applyControlClickPosition)
        except:
            if control_window == 0:
                showControl.configure(text='Relative Position: window does not exist')
            elif 'Any Window' in control_window:
                showControl.configure(text='Relative Position: window not selected')
            root.after(100,applyControlClickPosition)
    else:
        showControl.configure(text='')

showStatus = customtkinter.CTkLabel(master=root, text='Status: Stopped', font=('whitney',16))
showStatus.place(x=610, y=420)
showWarning = customtkinter.CTkLabel(master=root, text='Warning: None')
showWarning.place(x=210, y=420)
showMouse = customtkinter.CTkLabel(master=root)
showMouse.place(x=610, y=465)
showControl = customtkinter.CTkLabel(master=root)
showControl.place(x=350,y=465)

applyMousePosition()

def autoclicker():
    import win32con
    global times
    global pressButton
    def autoclicker_delay():
        global waiting
        if delay > 1000:
            waiting = time.monotonic()+((delay if offsetInterval == False else abs(delay+offset))*.001)
        else:
            time.sleep((delay if offsetInterval == False else abs(delay+offset))*.001)
    while True:
        if clicking and time.monotonic() >= waiting:
            if restrictingClicker:
                if 'Any Window' not in restrictClicker:
                    hwnd = win32gui.GetForegroundWindow()
                    if hwnd not in restrictClicker.values():
                        autoclicker_delay()
                        continue
            if repeating:
                if times >= repeats:
                    toggle_clicker('down')
                    continue
                else:
                    times = times + 1
            if customPosition and not ghostClick:
                autoit.mouse_move(x=MousepositionX,y=MousepositionY, speed=0)
            if offsetMouse:
                xoff = random.uniform(-MouseoffsetX,MouseoffsetX)
                yoff = random.uniform(-MouseoffsetY,MouseoffsetY)
                if not ghostClick:
                    pos = autoit.mouse_get_pos()
                    xoff = int(xoff+pos[0])
                    yoff = int(yoff+pos[1])
                    autoit.mouse_move(x=xoff,y=yoff, speed=0)
            if offsetInterval:
                offset = random.uniform(-Clickoffset,Clickoffset)
            if ghostClick:
                if pressButton == 'Right':
                    mouse_btn = win32con.MK_RBUTTON
                    mouse_btn_down = win32con.WM_RBUTTONDOWN
                    mouse_btn_up = win32con.WM_RBUTTONUP
                else:
                    mouse_btn = win32con.MK_LBUTTON
                    mouse_btn_down = win32con.WM_LBUTTONDOWN
                    mouse_btn_up = win32con.WM_LBUTTONUP
                if not offsetMouse:
                    yoff,xoff = 0,0
                lParam = MousepositionY+round(yoff) << 16| MousepositionX+round(xoff)
                subWindow.SendMessage(mouse_btn_down, mouse_btn, lParam)
                subWindow.SendMessage(mouse_btn_up, 0, lParam)
                subWindow.UpdateWindow()
                autoclicker_delay()
                continue
            if holding > 0:
                autoit.mouse_down(button=pressButton)
                holdtime = time.monotonic()+holding
                while True:
                    if time.monotonic() >= holdtime:
                        break
                    elif not clicking:
                        break
                    else:
                        time.sleep(1*.001)
                autoit.mouse_up(button=pressButton)
            elif clickingType == 1:
                autoit.mouse_click(button=pressButton)
            elif clickingType == 2:
                autoit.mouse_click(button=pressButton)
                autoit.mouse_click(button=pressButton)
            else:
                autoit.mouse_click(button=pressButton)
                autoit.mouse_click(button=pressButton)
                autoit.mouse_click(button=pressButton)
            if alternating:
                if pressButton=='Right':
                    pressButton = 'Left'
                else:
                    pressButton = 'Right'
            autoclicker_delay()
        else:
            if not clicking:
                root.title(title)
                time.sleep(100*.001)
            else:
                if mouseTimer:
                    m, s = divmod(round(waiting-time.monotonic()), 60)
                    h, m = divmod(m, 60)
                    root.title(f'{title} - Time until next click: {h:d}:{m:02d}:{s:02d}')
                time.sleep(1*.001)
        time.sleep(0.00000000000000000001)
def superclicker0():
    import pyautogui
    global waiting
    pyautogui.PAUSE=0
    pyautogui.FAILSAFE = False
    while True:
        if clicking and superClicker and time.monotonic() >= waiting:
            pyautogui.click(button=pressButton)
            if delay > 1000:
               waiting = time.monotonic()+(delay*.001)
            else:
                time.sleep((delay)*.001)
        else:
            if not superClicker and not clicking:
                time.sleep(100*.001)
            else:
                time.sleep(1*.001)
        time.sleep(0.00000000000000000001)

########### updater
def defaultupdatebutton():
    updateButton.configure(text=f'Version: {version}',text_color=('black', 'white'))
def downloader():
    import tempfile
    try:
        updateText.configure(text='Downloading')
        cancelButton.configure(state='disabled')
        downloadButton.configure(state='disabled')
        window.protocol("WM_DELETE_WINDOW", disable_event)
        downloadBar = customtkinter.CTkProgressBar(master=window)
        downloadBar.place(x=60,y=35)
        downloadBar.configure(mode='indeterminate')
        downloadBar.start()
        download = requests.get(f'https://github.com/Assassin654/AutoClicker/releases/download/{updateVersion}/AutoClickerMacroInstaller.exe', allow_redirects=True, timeout=5)
        os.chdir(tempfile.gettempdir())
        try:
            os.remove('AutoClickerMacroInstaller.exe')
        except:
            pass
        with open('AutoClickerMacroInstaller.exe', 'wb') as f:
            f.write(download.content)
        time.sleep(2)
        os.startfile('AutoClickerMacroInstaller.exe')
        Popen(['taskkill', '/f', '/t', '/pid', str(killSwitch.pid)], creationflags=CREATE_NO_WINDOW)
        os._exit(os.EX_OK)
    except:
        showWarning.configure(text='Warning: Was not able to download update, restart to try again', text_color='red')
        window.destroy()
downloadThread = threading.Thread(target=downloader, daemon=True)
def updater():
    global updateText
    global window
    global cancelButton
    global downloadButton
    try:
        update = requests.get('https://api.github.com/repos/Assassin654/AutoClicker/releases/latest', timeout=2)
        updateVersion = (update.json()["name"])
    
        if updateVersion != version:
            updateButton.configure(text_color=('#F4C430','yellow'))
            showWarning.configure(text='Warning: None', text_color=('black', 'white'))
            window = customtkinter.CTkToplevel()
            window.title('Updater')
            window.geometry('320x100')
            window.iconphoto(False, PhotoImage(file='gear.png'))
            window.attributes('-topmost',True)
            window.grab_set()
            window.resizable(False,False)
            updateText = customtkinter.CTkLabel(master=window, text=f'Latest version: {updateVersion}\tCurrent Version: {version}')
            updateText.pack(side='top',pady=10)
            cancelButton = customtkinter.CTkButton(master=window, text='Cancel', command=window.destroy)
            cancelButton.place(x=5,y=50)
            if 'W7' in version:
                downloadButton = customtkinter.CTkButton(master=window, text='Not Avaliable for W7', state='disabled')
            else:
                downloadButton = customtkinter.CTkButton(master=window, text='Update', command=downloadThread.start)
            downloadButton.place(x=175,y=50)
            window.mainloop()
        else:
            updateButton.configure(text='Version: Latest!', text_color='green')
            showWarning.configure(text='Warning: None', text_color=('black', 'white'))
            root.after(2000, defaultupdatebutton)
    except(requests.ConnectionError):
        showWarning.configure(text='Warning: No internet connection', text_color=('#F4C430','yellow'))
        window.destroy()
    except:
        showWarning.configure(text='Warning: API ratelimit on updates', text_color=('#F4C430','yellow'))
        window.destroy()

updateButton = customtkinter.CTkButton(master=root, text=f'Version: {version}',bg_color='transparent',fg_color='transparent', hover_color='grey', border_spacing = 0, width=0, command=updater, text_color=('black', 'white'))
updateButton.place(x=205, y=465)
settingsUpdateButton = customtkinter.CTkButton(master=settingFrame,text='Update', width=80, command=updater)
settingsUpdateButton.place(x=482,y=235)

get_window_list()
updateWindows(None)
applyControlClickPosition()

try:
    update = requests.get('https://api.github.com/repos/Assassin654/AutoClicker/releases/latest', timeout=2)
    updateVersion = (update.json()["name"])
    if updateVersion != version:
        updateButton.configure(text_color=('#F4C430','yellow'))
except:
    showWarning.configure(text='Warning: Could not check for latest version')

clickthread = threading.Thread(target=autoclicker)
clickthread.start()
recordMacroThread = threading.Thread(target=recordMacro)
recordMacroThread.start()
playMacroThread = threading.Thread(target=playMacro)
playMacroThread.start()
savingMacroThread = threading.Thread(target=saveMacro)
savingMacroThread.start()
superclickerThread = threading.Thread(target=superclicker0)

if superClicker:
    superclickerThread.start()
    disable_features_superclick()
    mil_interval.insert(0,'0')
    showWarning.configure(text='Warning: Super clicker enabled. some options are limited', text_color='orange')
else:
    mil_interval.insert(0,'1')

root.mainloop()
Popen(['taskkill', '/f', '/t', '/pid', str(killSwitch.pid)], creationflags=CREATE_NO_WINDOW)
os._exit(os.EX_OK)
#os._exit(0)
