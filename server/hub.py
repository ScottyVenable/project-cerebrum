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
from pylsl import StreamInlet, resolve_stream, StreamInfo, StreamOutlet
from scipy.signal import welch

class RealTimeHub(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # ... existing setup ...

        # New: Inference & Stability Stream
        info = StreamInfo('Cerebrum_Inference', 'Classification', 2, 0, 'float32', 'inf_001')
        self.outlet = StreamOutlet(info)

        # ... existing threading ...

    def update_data(self):
        while self.running:
            samples, timestamps = self.inlet.pull_chunk(timeout=1.0, max_samples=25)
            if samples:
                new_data = np.array(samples).T
                self.raw_buffer = np.roll(self.raw_buffer, -new_data.shape[1], axis=1)
                self.raw_buffer[:, -new_data.shape[1]:] = new_data

                # New: Real-time Stability Calculation (Alpha/Beta Ratio)
                freqs, psd = welch(new_data[0], fs=250, nperseg=min(new_data.shape[1], 256))
                alpha_idx = np.where((freqs >= 8) & (freqs <= 13))
                beta_idx = np.where((freqs >= 14) & (freqs <= 30))

                alpha_pow = np.mean(psd[alpha_idx]) if len(alpha_idx[0]) > 0 else 0
                beta_pow = np.mean(psd[beta_idx]) if len(beta_idx[0]) > 0 else 0

                # Stability = simple Alpha/Beta ratio normalized 0-1
                stability = alpha_pow / (alpha_pow + beta_pow + 1e-6)
                self.outlet.push_sample([0.5, stability]) # [Placeholder Class, Stability]


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
