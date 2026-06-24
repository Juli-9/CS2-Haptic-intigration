from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def gsi():
    data = request.json

    print("\n=== GSI UPDATE ===")

    player = data.get("player", {})

    # Health
    health = player.get("state", {}).get("health")
    print("Health:", health)

    # Map
    print("Map:", data.get("map", {}).get("name"))
    print("Phase:", data.get("map", {}).get("phase"))

    # Weapons deep parse
    weapons = player.get("weapons", {})

    print("\n--- WEAPONS ---")

    for key, w in weapons.items():
        name = w.get("name")
        state = w.get("state")
        ammo = w.get("ammo_clip")
        ammo_max = w.get("ammo_clip_max")
        reserve = w.get("ammo_reserve")

        print(f"{key}: {name}")
        print(f"  state: {state}")
        print(f"  ammo: {ammo}/{ammo_max} | reserve: {reserve}")

    return "OK", 200


if __name__ == "__main__":
    app.run(port=3000, threaded=True)