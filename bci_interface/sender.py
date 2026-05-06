import time
from pylsl import StreamInfo, StreamOutlet
import random

def start_sender():
    """
    Simulates or interfaces with the EEG hardware (e.g., PiEEG or Muse)
    and broadcasts the data over the local network using Lab Streaming Layer (LSL).
    """
    # Metadata: Name: RaspberryPi_EEG, Type: EEG, Channels: 8, Rate: 250Hz, Format: float32
    info = StreamInfo('RaspberryPi_EEG', 'EEG', 8, 250, 'float32', 'pi_eeg_001')
    
    # Create the LSL outlet
    outlet = StreamOutlet(info)
    print("Project Cerebrum: EEG LSL Outlet active. Broadcasting...")
    
    try:
        while True:
            # Placeholder for actual hardware SPI/I2C/BLE reading logic
            # Simulating raw microvolt signal for 8 channels
            sample = [random.uniform(-50.0, 50.0) for _ in range(8)]
            
            # Push to the local LSL network
            outlet.push_sample(sample)
            
            # 250Hz timing sync
            time.sleep(1.0 / 250.0)
    except KeyboardInterrupt:
        print("\n[BCI] LSL Sender terminated.")

if __name__ == "__main__":
    start_sender()
