import serial
import threading
from collections import deque

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore


PORT = "COM5"
BAUD = 74880

left_data = deque(maxlen=1000)
right_data = deque(maxlen=1000)
diff_data = deque(maxlen=1000)


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
            diff_data.append(left - right)

        except Exception as e:
            print(e)


app = QtWidgets.QApplication([])

win = pg.GraphicsLayoutWidget(
    title="ESP32 PWM Monitor",
    show=True
)

pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')
pg.setConfigOptions(antialias=True)

plot = win.addPlot()

# plot.showGrid(x=True, y=True, alpha=0.3)

plot.setLabel("left", "PWM")
plot.setLabel("bottom", "Samples")
plot.setYRange(0, 255)
plot.setXRange(0, 1000)

curve_left = plot.plot(
    pen=pg.mkPen('r', width=3, style=QtCore.Qt.SolidLine)
)

curve_right = plot.plot(
    pen=pg.mkPen('b', width=3, style=QtCore.Qt.SolidLine)
)

curve_diff = plot.plot(
    pen=pg.mkPen('y', width=3, style=QtCore.Qt.DotLine)
)

legend = plot.addLegend()
legend.addItem(curve_left, "PWM1")
legend.addItem(curve_right, "PWM2")
legend.addItem(curve_diff, "DIFF")


def update():

    curve_left.setData(list(left_data))
    curve_right.setData(list(right_data))
    curve_diff.setData(list(diff_data))


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)


threading.Thread(
    target=serial_thread,
    daemon=True
).start()

app.exec()