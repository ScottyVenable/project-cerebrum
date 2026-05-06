import mne
import pyxdf
import numpy as np
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

def analyze_calibration_data(xdf_path):
    """
    Processes raw XDF data from a calibration session.
    Applies bandpass filtering and Common Spatial Patterns (CSP).
    """
    print(f"[Analysis] Loading session: {xdf_path}")
    
    # 1. Load LSL Data
    streams, header = pyxdf.load_xdf(xdf_path)
    eeg_data = None
    marker_data = None
    
    for stream in streams:
        if stream['info']['type'][0] == 'EEG':
            eeg_data = stream
        elif stream['info']['type'][0] == 'Markers':
            marker_data = stream
            
    if eeg_data is None or marker_data is None:
        raise ValueError("Missing EEG or Marker stream in XDF file.")

    # 2. Convert to MNE Raw Object
    data = eeg_data['time_series'].T # (Channels, Samples)
    sfreq = float(eeg_data['info']['nominal_srate'][0])
    ch_names = [f"CH{i+1}" for i in range(data.shape[0])]
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
    raw = mne.io.RawArray(data, info)
    
    # 3. Preprocessing (1-40Hz Bandpass)
    print("[Analysis] Applying temporal filters...")
    raw.filter(1., 40., fir_design='firwin', skip_by_annotation='edge')
    
    # 4. Epoching (Extract trials based on markers)
    # This assumes markers are "TASK_LEFT_START", "TASK_RIGHT_START"
    events = mne.find_events(raw) # Custom logic needed to map markers to events
    event_id = {'left': 1, 'right': 2}
    epochs = mne.Epochs(raw, events, event_id, tmin=0.5, tmax=3.5, baseline=None, preload=True)
    
    # 5. Spatial Filtering (CSP)
    print("[Analysis] Calculating Common Spatial Patterns...")
    csp = CSP(n_components=4, reg=None, log=True, norm_trace=False)
    X = epochs.get_data()
    y = epochs.events[:, -1]
    
    # 6. Validation
    lda = LinearDiscriminantAnalysis()
    scores = cross_val_score(lda, csp.fit_transform(X, y), y, cv=5)
    
    print(f"\n--- Analysis Results ---")
    print(f"Mean Accuracy: {np.mean(scores)*100:.2f}%")
    print(f"Spatial patterns calculated and ready for inference.")
    
    # Plotting topographic maps (First 2 components)
    csp.plot_patterns(epochs.info, ch_type='eeg', units='uV', size=1.5)
    plt.show()

if __name__ == "__main__":
    # Placeholder for first run
    print("Neuro-Analysis module active. Run with path to .xdf file.")
