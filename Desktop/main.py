import time
from serial import Serial
from serial.tools import list_ports
from state_engine import StateEngine
from plotter import Plotter
import logging
logging.getLogger("werkzeug").setLevel(logging.WARNING)

PLOT_QUEUE_SIZE = 200
BAUD = 230400   

def select_port() -> str:
    ports = list(list_ports.comports())

    if not ports:
        raise RuntimeError("Kein COM-Port gefunden.")

    if len(ports) == 1:
        port = ports[0].device
        print(f"Verwende automatisch: {port}")
        return port

    print("Mehrere COM-Ports gefunden:")
    for i, port in enumerate(ports, start=1):
        print(f"{i}: {port.device} ({port.description})")

    while True:
        try:
            choice = int(input("Port auswählen: "))
            if 1 <= choice <= len(ports):
                return ports[choice - 1].device
        except ValueError:
            pass

        print("Ungültige Eingabe.")


def main() -> int:

    port = select_port()
    ser = Serial(port, BAUD)

    se: StateEngine = StateEngine(ser=ser)
    plt: Plotter = Plotter(queue_size=PLOT_QUEUE_SIZE, ser=ser)

    se.start()

    try: 
        plt.start()

    except KeyboardInterrupt: print("^C)" + "\n")

    except Exception as e:print(e)

    finally:

        if plt and plt.running: plt.stop()

        if se and se.running: se.stop()

        if ser and ser.is_open: ser.close()


    print("------------------------ MAIN THREAD CLOSED ------------------------\n")

    return 0

if __name__ == "__main__": main()
    