import subprocess
import time
import os
import signal

def run_test():
    print("--- [TEST] Starting Project Cerebrum Pipeline Validation ---")
    
    # 1. Start the LSL Sender in the background
    print("[TEST] Launching EEG Sender...")
    sender_proc = subprocess.Popen(['python3', 'bci_interface/sender.py'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   cwd='/root/Coding/projects/project-cerebrum')
    
    time.sleep(3) # Give LSL time to resolve
    
    # 2. Start the Hub in the background
    print("[TEST] Launching BCI Hub...")
    hub_proc = subprocess.Popen(['python3', 'server/hub.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 cwd='/root/Coding/projects/project-cerebrum')
    
    time.sleep(10) # Run for 10 seconds to collect logs
    
    # 3. Shutdown
    print("[TEST] Shutting down processes...")
    os.kill(sender_proc.pid, signal.SIGINT)
    os.kill(hub_proc.pid, signal.SIGINT)
    
    # 4. Analyze logs (simplistic check)
    hub_out, hub_err = hub_proc.communicate()
    sender_out, sender_err = sender_proc.communicate()
    
    print("\n--- [HUB LOGS] ---")
    print(hub_out.decode())
    
    if b"Buffer Processed" in hub_out:
        print("\n[SUCCESS] Data pipeline is functional. LSL streams resolved and processed.")
    else:
        print("\n[FAILURE] Data pipeline did not process buffers correctly.")
        print("ERRORS:", hub_err.decode())

if __name__ == "__main__":
    run_test()
