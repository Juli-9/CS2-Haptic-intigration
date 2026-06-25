from collections import deque
import serial
import threading
import queue

from pyqtgraph.Qt import QtWidgets, QtCore
import pyqtgraph as pg


class Plotter:

    def __init__(self, queue_size: int, ser: serial.Serial):

        # CONFIG
        self.queue_size = queue_size
        self.ser = ser

        self.running = True

        # THREAD-SAFE BUFFER
        self.data_queue = queue.Queue(maxsize=1000)

        # GUI buffers (only used in GUI thread!)
        self.left_data = deque(maxlen=queue_size)
        self.right_data = deque(maxlen=queue_size)
        self.diff_data = deque(maxlen=queue_size)

        # QT APP
        self.app: QtWidgets.QApplication = QtWidgets.QApplication([])

        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')

        self.win = pg.GraphicsLayoutWidget(title="ESP32 PWM Monitor", show=True)
        self.plot = self.win.addPlot()

        self.plot.setLabel("left", "PWM")
        self.plot.setLabel("bottom", "Samples")
        self.plot.setYRange(0, 255)
        self.plot.setXRange(0, queue_size)

        self.curve_diff = self.plot.plot(pen=pg.mkPen('y', width=3, style=QtCore.Qt.DotLine))
        self.curve_left = self.plot.plot(pen=pg.mkPen('r', width=4))
        self.curve_right = self.plot.plot(pen=pg.mkPen('b', width=4))

        legend = self.plot.addLegend()
        legend.addItem(self.curve_left, "PWM1")
        legend.addItem(self.curve_right, "PWM2")
        legend.addItem(self.curve_diff, "DIFF")

        # TIMER (GUI THREAD ONLY)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(18)

    # START
    def start(self):
        threading.Thread(target=self.serial_thread, daemon=True).start()
        self.app.exec()

    # SERIAL THREAD (ONLY IO + QUEUE PUSH)
    def serial_thread(self):
        while self.running:
            try:
                line = self.ser.readline().decode(errors="ignore").strip()
                if not line: continue

                left, right = map(int, line.split(","))

                # non-blocking push
                try: self.data_queue.put_nowait((left, right))
                except queue.Full: pass

            except Exception as e: print("Serial error:", e)

    # GUI UPDATE (ONLY THREAD-SAFE CONSUMPTION)
    def update(self):

        if not self.running: return

        # Drain queue
        while not self.data_queue.empty():
            left, right = self.data_queue.get()

            self.left_data.append(left)
            self.right_data.append(right)
            self.diff_data.append(left - right)

        # Update plots
        self.curve_left.setData(list(self.left_data))
        self.curve_right.setData(list(self.right_data))
        self.curve_diff.setData(list(self.diff_data))

    def stop(self):
        self.running = False
        self.timer.stop()
        self.app.closeAllWindows()
        self.app.quit()