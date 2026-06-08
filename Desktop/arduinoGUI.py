import tkinter as tk
import json
import serial

#------------Arduino connection--------------

ser = serial.Serial("COM6", 9600)

dataToSend = {
    "isFiring": False,
    "firingPeriod": 10,
    "firingPattern": 0,
    "ammunitionPercent": 0,
    "intensityPercent": 0
}

#-----------------Functions-----------------

def updateOutput():
    line = ser.readline()
    if line:
        text = line.decode('utf-8').strip()
        if text:
            print(text)

def vibrationON():
    dataToSend["isFiring"] = True
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    updateOutput()
def vibrationOFF():
    dataToSend["isFiring"] = False
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    updateOutput()
def updateAmmoPercent(val):
    dataToSend["ammunitionPercent"] = int(val)
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    updateOutput()
def updatePattern(val):
    dataToSend["firingPattern"] = int(val)
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    updateOutput()
def updateIntensity(val):
    dataToSend["intensityPercent"] = int(val)
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    updateOutput()
def updatePeriod(val):
    dataToSend["firingPeriod"] = int(val)
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    updateOutput()

#Sine, SawUp, SawDown, HeavyShot

#------------GUI-------------
win = tk.Tk()
win.title("CS haptic feedback debug")
win.minsize(240,240)

buttonLabel = tk.Label(win, text="Click to turn ON/OFF")
buttonLabel.grid(column=1, row=1)

ONbtn = tk.Button(win, bd=4, text="TEST AR ON", command=vibrationON)
ONbtn.grid(column=1, row=2)
OFFbtn = tk.Button(win, bd=4, text="TEST AR OFF", command=vibrationOFF)
OFFbtn.grid(column=2, row=2)

ammoVal = tk.IntVar()
AMMOPercent = tk.Scale(win, bd=5, from_=0, to=100, orient=tk.HORIZONTAL, command=updateAmmoPercent)
AMMOPercent.grid(column=1, row=3)
tk.Label(win, text="Ammo (%)").grid(column=2, row=3)

FIRINGPattern = tk.Scale(win, bd=5, from_=0, to=4, orient=tk.HORIZONTAL, command=updatePattern)
FIRINGPattern.grid(column=1, row=5)
tk.Label(win, text="0 = Constant; 1 = SinePulse;\n2 = SawUp; 3 = SawDown; 4 = HeavyShot").grid(column=2, row=5)

INTENSITYPercent = tk.Scale(win, bd=5, from_=0, to=100, orient=tk.HORIZONTAL, command=updateIntensity)
INTENSITYPercent.grid(column=1, row=7)
tk.Label(win, text="Intensity (%)").grid(column=2, row=7)

FIRINGPeriod = tk.Scale(win, bd=5, from_=10, to=2000, orient=tk.HORIZONTAL, command=updatePeriod)
FIRINGPeriod.grid(column=1, row=9)
tk.Label(win, text="Firing period (ms)").grid(column=2, row=9)

win.mainloop()
