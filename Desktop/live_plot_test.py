import serial
import threading
from collections import deque

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore


PORT = "COM5"
BAUD = 921600

left_data = deque(maxlen=1000)
right_data = deque(maxlen=1000)


def serial_thread():

    ser = serial.Serial(PORT, BAUD)

    while True:

        try:
            line = ser.readline().decode().strip()

            if not line:
                continue

            left, right = map(int, line.split(","))

            left_data.append(left)
            right_data.append(right)

        except Exception as e:
            print(e)


app = QtWidgets.QApplication([])

win = pg.GraphicsLayoutWidget(
    title="ESP32 PWM Monitor",
    show=True
)

plot = win.addPlot()

plot.setLabel("left", "PWM")
plot.setLabel("bottom", "Samples")

curve_left = plot.plot(pen=pg.mkPen(color="r", width=2), name="Left")
curve_right = plot.plot(pen=pg.mkPen(color="b", width=2), name="Right")


def update():

    curve_left.setData(list(left_data))
    curve_right.setData(list(right_data))


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)


threading.Thread(
    target=serial_thread,
    daemon=True
).start()

app.exec()