"""
CS2 Haptic Bridge
=================

Blueprint / Architekturvorlage

Datenfluss:

CS2 GameState
      │
      ▼
 StateEngine
      │
      ▼
 SerialManager
      │
      ├── JSON -> ESP32
      │
      └── PWM <- ESP32
                 │
                 ▼
              Plotter
"""

import json
import threading
from dataclasses import dataclass

import serial

# ============================================================
# Pattern IDs
# ============================================================

PATTERN_CONSTANT = 0
PATTERN_SINE = 1
PATTERN_SAW_UP = 2
PATTERN_SAW_DOWN = 3


# ============================================================
# Lookup Table
# ============================================================

WEAPON_TABLE = {
    "ak47": {"pattern": PATTERN_SAW_DOWN, "period_ms": 100, "one_shot": False},
    "m4a1": {"pattern": PATTERN_SAW_DOWN, "period_ms": 85, "one_shot": False},
    "usp_silencer": {"pattern": PATTERN_CONSTANT, "period_ms": 80, "one_shot": True},
}


# ============================================================
# Haptic State
# ============================================================


@dataclass
class HapticState: 

    enabled: bool
    pattern: int
    period_ms: int
    one_shot: bool

    def to_dict(self):

        return {
            "enabled": self.enabled,
            "pattern": self.pattern,
            "period_ms": self.period_ms,
            "one_shot": self.one_shot,
        }


# ============================================================
# Plotter
# ============================================================


class Plotter:

    def __init__(self):

        self.left_buffer = []
        self.right_buffer = []

        self.max_samples = 1000

    def add_sample(self, left_pwm: int, right_pwm: int):

        self.left_buffer.append(left_pwm)
        self.right_buffer.append(right_pwm)

        if len(self.left_buffer) > self.max_samples:
            self.left_buffer.pop(0)

        if len(self.right_buffer) > self.max_samples:
            self.right_buffer.pop(0)

        # TODO:
        # pyqtgraph update

    def update(self):

        pass


# ============================================================
# Serial Manager
# ============================================================


class SerialManager:

    def __init__(self, port: str, baudrate: int, plotter: Plotter):

        self.plotter = plotter

        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)

        self.reader_thread = threading.Thread(target=self.read_loop, daemon=True)

        self.reader_thread.start()

    # --------------------------------------------------------

    def send_state(self, state: HapticState):

        packet = json.dumps(state.to_dict())

        self.ser.write((packet + "\n").encode())

    # --------------------------------------------------------

    def read_loop(self):

        while True:

            try:

                line = self.ser.readline().decode().strip()

                if not line:
                    continue

                self.handle_line(line)

            except Exception as e:

                print(f"[Serial RX Error] {e}")

    # --------------------------------------------------------

    def handle_line(self, line: str):
        """
        Erwartet:

        123,87
        """

        try:

            left, right = map(int, line.split(","))

            self.plotter.add_sample(left, right)

        except Exception:

            print(f"[Malformed PWM Packet] {line}")


# ============================================================
# State Engine
# ============================================================


class StateEngine:

    def __init__(self, serial_manager: SerialManager):

        self.serial_manager = serial_manager

        self.current_weapon = None
        self.is_firing = False

    # --------------------------------------------------------

    def update_from_gamestate(self, gs: dict):
        """
        Wird vom HTTP Receiver
        aufgerufen.
        """

        weapon = self.extract_weapon(gs)

        firing = self.extract_firing(gs)

        state = self.build_haptic_state(weapon, firing)

        self.serial_manager.send_state(state)

    # --------------------------------------------------------

    def extract_weapon(self, gs: dict) -> str:

        #
        # TODO:
        # echte CS2-Auswertung
        #

        return gs.get("weapon", "ak47")

    # --------------------------------------------------------

    def extract_firing(self, gs: dict) -> bool:

        #
        # TODO:
        # echte Schusserkennung
        #

        return gs.get("firing", False)

    # --------------------------------------------------------

    def build_haptic_state(self, weapon: str, firing: bool) -> HapticState:

        if not firing:

            return HapticState(
                enabled=False, pattern=PATTERN_CONSTANT, period_ms=0, one_shot=False
            )

        cfg = WEAPON_TABLE.get(weapon)

        if cfg is None:

            return HapticState(
                enabled=False, pattern=PATTERN_CONSTANT, period_ms=0, one_shot=False
            )

        return HapticState(
            enabled=True,
            pattern=cfg["pattern"],
            period_ms=cfg["period_ms"],
            one_shot=cfg["one_shot"],
        )


# ============================================================
# GameState Receiver
# ============================================================


class GameStateReceiver:

    def __init__(self, state_engine: StateEngine):

        self.state_engine = state_engine

    def on_gamestate(self, data: dict):

        self.state_engine.update_from_gamestate(data)


# ============================================================
# Application
# ============================================================


class Application:

    def __init__(self):

        self.plotter = Plotter()

        self.serial_manager = SerialManager(
            port="COM5", baudrate=921600, plotter=self.plotter
        )

        self.state_engine = StateEngine(self.serial_manager)

        self.receiver = GameStateReceiver(self.state_engine)

    def run(self):

        print("CS2 Haptic Bridge started.")

        #
        # TODO:
        # Flask/FastAPI starten
        #

        while True:
            pass


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    app = Application()

    app.run()
