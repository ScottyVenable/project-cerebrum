import tkinter as tk
import time
import random
from pylsl import StreamInfo, StreamOutlet

class CalibrationApp:
    """
    A simple UI to guide the user through the Motor Imagery Graz Paradigm.
    Broadcasts markers via LSL to synchronize with the EEG data.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cerebrum: Calibration")
        self.root.geometry("600x400")
        self.root.configure(bg='black')
        
        self.label = tk.Label(self.root, text="+", font=("Helvetica", 60), fg="white", bg="black")
        self.label.pack(expand=True)
        
        # Setup LSL Marker Stream
        # In a real environment, pylsl must be installed.
        try:
            info = StreamInfo('Cerebrum_Markers', 'Markers', 1, 0, 'string', 'marker_id_001')
            self.outlet = StreamOutlet(info)
            self.lsl_enabled = True
        except:
            print("[Warning] LSL not found. Running in UI-only mode.")
            self.lsl_enabled = False
        
        self.tasks = ["LEFT", "RIGHT"] * 20
        random.shuffle(self.tasks)
        
    def send_marker(self, marker):
        print(f"Marker: {marker}")
        if self.lsl_enabled:
            self.outlet.push_sample([marker])

    def start_session(self):
        for task in self.tasks:
            # 1. Rest
            self.label.config(text="+", fg="white")
            self.root.update()
            self.send_marker("REST_START")
            time.sleep(2)
            
            # 2. Cue
            cue_text = "<--" if task == "LEFT" else "-->"
            self.label.config(text=cue_text, fg="cyan")
            self.root.update()
            self.send_marker(f"CUE_{task}")
            time.sleep(1.25)
            
            # 3. Task
            self.label.config(fg="purple") # Imagery Phase
            self.root.update()
            self.send_marker(f"TASK_{task}_START")
            time.sleep(4)
            
            # 4. Break
            self.label.config(text="", fg="white")
            self.root.update()
            self.send_marker("TRIAL_END")
            time.sleep(1.5)
            
        self.label.config(text="Session Complete", font=("Helvetica", 30))
        self.root.update()

if __name__ == "__main__":
    app = CalibrationApp()
    app.root.after(2000, app.start_session)
    app.root.mainloop()
