import sys
import numpy as np
from pylsl import StreamInlet, resolve_stream
from scipy.signal import butter, lfilter
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import threading
import time

# Configuration
CHANNELS = 8
FS = 250
WINDOW_SEC = 2
SAMPLES = int(FS * WINDOW_SEC)

class RealTimeHub(QtWidgets.QMainWindow):
    """
    Professional BCI Hub: Multi-threaded processing and visualization.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Cerebrum: Real-Time Hub")
        self.central_widget = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.central_widget)
        
        # Setup Plots for 8 channels
        self.plots = []
        self.curves = []
        for i in range(CHANNELS):
            p = self.central_widget.addPlot(row=i, col=0)
            p.setLabel('left', f'CH {i+1}')
            self.plots.append(p)
            self.curves.append(p.plot(pen='c'))
            
        # Data Buffers
        self.raw_buffer = np.zeros((CHANNELS, SAMPLES))
        
        # LSL Connection
        print("[Hub] Resolving EEG Stream...")
        streams = resolve_stream('type', 'EEG')
        self.inlet = StreamInlet(streams[0])
        
        # Threading for Ingestion
        self.running = True
        self.ingest_thread = threading.Thread(target=self.update_data, daemon=True)
        self.ingest_thread.start()
        
        # Timer for UI Update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50) # 20 FPS Update

    def update_data(self):
        """Background thread to pull data from LSL without blocking UI."""
        while self.running:
            samples, timestamps = self.inlet.pull_chunk(timeout=1.0, max_samples=25)
            if samples:
                new_data = np.array(samples).T
                self.raw_buffer = np.roll(self.raw_buffer, -new_data.shape[1], axis=1)
                self.raw_buffer[:, -new_data.shape[1]:] = new_data

    def update_plot(self):
        """Updates the PyQtGraph curves."""
        for i in range(CHANNELS):
            # Applying a simple visual offset for clarity
            self.curves[i].setData(self.raw_buffer[i])

    def closeEvent(self, event):
        self.running = False
        super().closeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    hub = RealTimeHub()
    hub.show()
    sys.exit(app.exec_())
