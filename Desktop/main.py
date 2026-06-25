import time
from serial import Serial
from state_engine import StateEngine
from plotter import Plotter
import logging
logging.getLogger("werkzeug").setLevel(logging.WARNING)

PLOT_QUEUE_SIZE = 200
PORT = "COM5"
BAUD = 74880

def main() -> int:

    ser: Serial = Serial(PORT, BAUD)

    se: StateEngine = StateEngine(ser=ser)
    plt: Plotter = Plotter(baud=BAUD, port=PORT, queue_size=PLOT_QUEUE_SIZE, ser=ser)

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
    