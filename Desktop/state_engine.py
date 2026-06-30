import json
import threading
import time
import flask
import serial
import numpy as np

from weapon_data import WEAPON_DATA

from ctypes import windll

VK_LBUTTON = 0x01

def is_left_mouse_pressed(): return bool(windll.user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000)

class StateEngine:

    def __init__(self, ser: serial.Serial):

        self.ser = ser
        self.running = False

        self.app = flask.Flask(__name__)

        # Route sauber registrieren
        self.app.add_url_rule(
            "/",
            "gsi",
            self.gsi,
            methods=["POST"]
        )

        self.server_thread = None

        self.prev_ammo: int = 0
        self.game_state: dict = {
        "activeWeaponName" : "",
        "ammoRatio": 0.0,
        "ammoReduced" : False,
        "alive" : False
        }

        self.state: dict = {
            "isFiring": False,
            "firingPeriod": 10,
            "firingPattern": 0,
            "ammunitionPercent": 0,
            "intensityPercent": 50,
            "oneShot" : False
        }

        self.prev_weapon_name: str = ""

        self.ammo_reduced_once = False
        self.prev_state = self.state.copy()

        self.state_lock = threading.Lock()
        self.game_state_lock = threading.Lock()


    # START
    def start(self):

        self.running = True

        self.server_thread = threading.Thread(
            target=self.run_server,
            daemon=True
        )

        self.server_thread.start()

        self.state_thread = threading.Thread(
            target=self.state_thread,
            daemon=True
        )

        self.state_thread.start()


    def update_state(self):
        with self.game_state_lock:
            name = self.game_state["activeWeaponName"]
            ammo_reduced = self.game_state["ammoReduced"]
            ammo = int(self.game_state["ammoRatio"] * 100)

            self.game_state["ammoReduced"] = False

        weapon = WEAPON_DATA.get(name)

        if weapon is None:
            is_firing = False
        elif self.prev_weapon_name != name:
            is_firing = False
        elif weapon["oneShot"]:
            is_firing = ammo_reduced
        else:
            if ammo_reduced:
                self.ammo_reduced_once = True
                is_firing = True

            elif is_left_mouse_pressed() and ammo > 0:
                is_firing = self.ammo_reduced_once
            else:
                is_firing = False
                self.ammo_reduced_once = False  

        self.prev_weapon_name = name

        if self.prev_state["oneShot"] and not is_firing: return

        with self.state_lock:
            self.state["isFiring"] = is_firing
            self.state["ammunitionPercent"] = ammo
            self.state["intensityPercent"] = int(weapon["intensity"] * 100.0)

            if weapon is None:
                self.state["oneShot"] = False
            else:
                self.state["firingPeriod"] = round(1000 / weapon["hz"])
                self.state["firingPattern"] = weapon["firingPattern"]
                self.state["oneShot"] = weapon["oneShot"]

            if self.state["oneShot"] and self.state["isFiring"] or self.state != self.prev_state:
                state = (json.dumps(self.state) + "\n").encode()
                self.ser.write(state)
                print(self.state)
                print("------------------------")

            self.prev_state = self.state.copy() 

    def state_thread(self):
        while self.running:
            self.update_state()
            time.sleep(0.01)  # 100 Hz

    # FLASK SERVER
    def run_server(self):

        self.app.run(
            port=3000,
            threaded=True,
            use_reloader=False
        )

    def stop(self):
        self.running = False

    def gsi(self):

        data = flask.request.json or {}

        player = data.get("player", {})
        alive = player["state"]["health"] > 0
        weapons = player.get("weapons", {})

        for key, w in weapons.items():
            with self.game_state_lock:
                if w.get("state") == "active":
                    self.game_state["activeWeaponName"] = w.get("name")

                    if not WEAPON_DATA.get(self.game_state["activeWeaponName"]):
                        continue
                    
                    self.game_state["alive"] = alive
                    ammo_clip = w.get("ammo_clip")
                    ammo_clip_max = w.get("ammo_clip_max")
                    self.game_state["ammoRatio"] =  ammo_clip / ammo_clip_max if ammo_clip_max > 0 else 0.0

                    if(self.prev_ammo > ammo_clip): 
                        self.game_state["ammoReduced"] = True

                    self.prev_ammo = ammo_clip

                    return "OK", 200


                self.game_state["activeWeaponName"] = ""
               
               


        return "OK", 200
