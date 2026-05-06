import numpy as np
from pylsl import StreamInlet, resolve_stream
from scipy.signal import butter, lfilter
import time

# Configuration
CHANNELS = 8
FS = 250        # Sampling Rate in Hz
LOWCUT = 1.0    # Hz
HIGHCUT = 40.0  # Hz
WINDOW_SEC = 1
SAMPLES = int(FS * WINDOW_SEC)

class CerebrumHub:
    """
    Central Raspberry Pi processing node. 
    Connects to LSL, filters data, and prepares for AI inference.
    """
    def __init__(self):
        print("[Hub] Resolving EEG stream on network...")
        streams = resolve_stream('type', 'EEG')
        if not streams:
            raise RuntimeError("No EEG stream found. Ensure sender.py is running.")
        
        self.inlet = StreamInlet(streams[0])
        self.buffer = np.zeros((CHANNELS, SAMPLES))
        print(f"[Hub] Connected to: {streams[0].name()}")

    def _butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def apply_filter(self, data):
        """Applies a Butterworth bandpass filter to the data buffer."""
        b, a = self._butter_bandpass(LOWCUT, HIGHCUT, FS, order=4)
        # Apply filter along the time axis (axis=1)
        return lfilter(b, a, data, axis=1)

    def normalize(self, data):
        """Z-score normalization."""
        mu = np.mean(data, axis=1, keepdims=True)
        sigma = np.std(data, axis=1, keepdims=True)
        return (data - mu) / (sigma + 1e-6)

    def listen(self):
        print(f"[Hub] Real-time loop active ({LOWCUT}-{HIGHCUT}Hz bandpass).")
        try:
            while True:
                # Pull new samples
                samples, timestamps = self.inlet.pull_chunk(timeout=1.0, max_samples=SAMPLES)
                if not samples:
                    continue
                
                # Update rolling buffer
                new_data = np.array(samples).T
                self.buffer = np.roll(self.buffer, -new_data.shape[1], axis=1)
                self.buffer[:, -new_data.shape[1]:] = new_data
                
                # Processing Pipeline
                filtered = self.apply_filter(self.buffer)
                normalized = self.normalize(filtered)
                
                # Reshape for EEGNet inference: (1, Channels, Samples, 1)
                input_tensor = normalized[np.newaxis, :, :, np.newaxis]
                
                # Status Report
                print(f"[Hub] Buffer Processed | Last TS: {timestamps[-1]:.2f} | Input Shape: {input_tensor.shape}")
                
                # Avoid hammering the CPU in the prototype phase
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n[Hub] Processing Hub stopped.")

if __name__ == "__main__":
    try:
        hub = CerebrumHub()
        hub.listen()
    except Exception as e:
        print(f"[Hub] Failure: {e}")
