import time
import requests

while True:

    print("reloading..")
    time.sleep(1)
    print("reloading done")

    ammo_max = 20
    ammo = ammo_max 

    while ammo >= 0:

        data = {
            "player": {
                "weapons": {
                    "weapon_0": {
                        "name": "weapon_m4a1_silencer",
                        "state": "active",
                        "ammo_clip": ammo,
                        "ammo_clip_max": ammo_max 
                    }
                }
            }
        }

        requests.post("http://127.0.0.1:3000", json=data)

        ammo -= 1
        time.sleep(1.0 / 10.0)
        # time.sleep(.5)
