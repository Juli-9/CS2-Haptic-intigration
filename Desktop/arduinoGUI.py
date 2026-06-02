from enum import Enum, auto
import tkinter as tk
import json
import serial

class FiringPattern(Enum):
    CONSTANT = auto()
    SINEPULSE = auto()
    SAWUP = auto()
    SAWDOWN = auto()
    HEAVYSHOT = auto()

#------------Arduino connection--------------

ser = serial.Serial("COM5", 115200)

dataToSend = {
    "isFiring": False,
    "firingPeriod": 100,
    "firingPattern": 0,
    "ammunitionPercent": 0
}

#-----------------Functions-----------------

def vibrationON():
    dataToSend["isFiring"] = True
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
def vibrationOFF():
    dataToSend["isFiring"] = False
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
def setAmmoPercent():
    dataToSend["ammunitionPercent"] = float(AMMOPercent.get())
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
def updatePattern():
    patternToMatch:str = str(FIRINGPattern.get())
    match patternToMatch:
        case "Constant":
            dataToSend["firingPattern"] = FiringPattern.CONSTANT.value
        case "SinePulse":
            dataToSend["firingPattern"] = FiringPattern.SINEPULSE.value
        case "SawUp":
            dataToSend["firingPattern"] = FiringPattern.SAWUP.value
        case "SawDown":
            dataToSend["firingPattern"] = FiringPattern.SAWDOWN.value
        case "HeavyShot":
            dataToSend["firingPattern"] = FiringPattern.HEAVYSHOT.value
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())

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

AMMOPercent = tk.Scale(win, bd=5, from_=0, to=100, orient=tk.HORIZONTAL)
AMMOPercent.grid(column=1, row=3)
tk.Label(win, text="Ammo (%)").grid(column=2, row=3)
AMMOPercentUpdate = tk.Button(win, bd=4, text="Update", command=setAmmoPercent)
AMMOPercentUpdate.grid(column=1, row=4)

FIRINGPattern = tk.Entry(win, bd=6, width=12)
FIRINGPattern.grid(column=1, row=5)
tk.Label(win, text="Choose firing pattern").grid(column=2, row=5)
FIRINGPatternUpdate = tk.Button(win, bd=4, text="Update", command=updatePattern)
FIRINGPatternUpdate.grid(column=1, row=6)

win.mainloop()
