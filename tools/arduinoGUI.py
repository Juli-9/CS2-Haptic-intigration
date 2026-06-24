import tkinter as tk
import json
import serial
import time

#------------Arduino connection--------------

ser = serial.Serial("COM5", 74880)

dataToSend = {
    "isFiring": False,
    "firingPeriod": 10,
    "firingPattern": 0,
    "ammunitionPercent": 0,
    "intensityPercent": 0,
    "oneShot" : False
}

# Wird eigentlich nur für Scopen verwendet, unwichtig auf Arduino
prevDataToSend = {
    "isFiring": False,
    "firingPeriod": 10,
    "firingPattern": 0,
    "ammunitionPercent": 0,
    "intensityPercent": 0,
    "oneShot" : False
}

#-----------------Functions-----------------

def saveData():
    prevDataToSend["isFiring"] = dataToSend["isFiring"]
    prevDataToSend["firingPeriod"] = dataToSend["firingPeriod"]
    prevDataToSend["firingPattern"] = dataToSend["firingPattern"]
    prevDataToSend["ammunitionPercent"] = dataToSend["ammunitionPercent"]
    prevDataToSend["intensityPercent"] = dataToSend["intensityPercent"]
    prevDataToSend["oneShot"] = dataToSend["oneShot"]


def loadData():
    dataToSend["isFiring"] = prevDataToSend["isFiring"]
    dataToSend["firingPeriod"] = prevDataToSend["firingPeriod"]
    dataToSend["firingPattern"] = prevDataToSend["firingPattern"]
    dataToSend["ammunitionPercent"] = prevDataToSend["ammunitionPercent"]
    dataToSend["intensityPercent"] = prevDataToSend["intensityPercent"]
    dataToSend["oneShot"] = prevDataToSend["oneShot"]

def vibrationON():
    dataToSend["isFiring"] = True
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    print(dataToSend)

def vibrationOFF():
    dataToSend["isFiring"] = False
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    print(dataToSend)

def scopeONCE():
    saveData()
    dataToSend["isFiring"] = True
    dataToSend["ammunitionPercent"] = 100
    dataToSend["firingPeriod"] = 25
    dataToSend["intensityPercent"] = 100
    dataToSend["firingPattern"] = 0
    dataToSend["oneShot"] = True
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    # time.sleep(0.025)
    # dataToSend["isFiring"] = False
    # json_string:str = json.dumps(dataToSend) + "\n"
    # ser.write(json_string.encode())
    print(dataToSend)
    loadData()

def scopeTWICE():
    scopeONCE()
    time.sleep(0.25)
    scopeONCE()

def updateAmmoPercent(val):
    dataToSend["ammunitionPercent"] = int(val)
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    print(dataToSend)

def updatePattern(val):
    dataToSend["firingPattern"] = int(val)
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    print(dataToSend)

def updateIntensity(val):
    dataToSend["intensityPercent"] = int(val)
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    print(dataToSend)

def updatePeriod(val):
    dataToSend["firingPeriod"] = int(val)
    json_string:str = json.dumps(dataToSend) + "\n"
    ser.write(json_string.encode())
    print(dataToSend)

#Sine, SawUp, SawDown, HeavyShot

#------------GUI-------------
win = tk.Tk()
win.title("CS haptic feedback debug")
win.minsize(240,240)

ONbtn = tk.Button(win, bd=4, text="Firing ON", command=vibrationON)
ONbtn.grid(column=1, row=1)
OFFbtn = tk.Button(win, bd=4, text="Firing OFF", command=vibrationOFF)
OFFbtn.grid(column=2, row=1)

tk.Label(win, text="").grid(column=1, row=2)

SCOPEONCEbtn = tk.Button(win, bd=4, text="Scope once", command=scopeONCE)
SCOPEONCEbtn.grid(column=1, row=3)
SCOPETWICEbtn = tk.Button(win, bd=4, text="Scope twice", command=scopeTWICE)
SCOPETWICEbtn.grid(column=2, row=3)

AMMOPercent = tk.Scale(win, bd=5, from_=0, to=100, orient=tk.HORIZONTAL, command=updateAmmoPercent)
AMMOPercent.grid(column=1, row=4)
tk.Label(win, text="Ammo (%)").grid(column=2, row=4)

FIRINGPattern = tk.Scale(win, bd=5, from_=0, to=4, orient=tk.HORIZONTAL, command=updatePattern)
FIRINGPattern.grid(column=1, row=5)
tk.Label(win, text="0 = Constant; 1 = SinePulse;\n2 = SawUp; 3 = SawDown; 4 = HeavyShot").grid(column=2, row=5)

INTENSITYPercent = tk.Scale(win, bd=5, from_=0, to=100, orient=tk.HORIZONTAL, command=updateIntensity)
INTENSITYPercent.grid(column=1, row=6)
tk.Label(win, text="Intensity (%)").grid(column=2, row=6)

FIRINGPeriod = tk.Scale(win, bd=5, from_=10, to=2000, orient=tk.HORIZONTAL, command=updatePeriod)
FIRINGPeriod.grid(column=1, row=7)
tk.Label(win, text="Firing period (ms)").grid(column=2, row=7)

win.mainloop()
