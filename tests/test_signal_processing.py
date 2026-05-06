import pytest
import numpy as np
from server.hub import CerebrumHub

def test_butter_bandpass_stability():
    hub = CerebrumHub()
    # Create 1 second of 50Hz noise (should be filtered out)
    fs = 250
    t = np.linspace(0, 1, fs)
    noise_50hz = np.sin(2 * np.pi * 50 * t)
    data = np.tile(noise_50hz, (8, 1))
    
    filtered = hub.apply_filter(data)
    
    # Check if the 50Hz noise is significantly attenuated
    # (Input was amp 1.0, filtered should be much lower)
    assert np.max(np.abs(filtered)) < 0.1

def test_normalization_output():
    hub = CerebrumHub()
    data = np.random.normal(100, 50, (8, 250)) # Mean 100, Std 50
    normalized = hub.normalize(data)
    
    # After Z-score, mean should be ~0 and std should be ~1
    for i in range(8):
        assert np.isclose(np.mean(normalized[i]), 0, atol=1e-5)
        assert np.isclose(np.std(normalized[i]), 1, atol=1e-5)

def test_buffer_reshaping():
    hub = CerebrumHub()
    data = np.zeros((8, 250))
    normalized = hub.normalize(data)
    input_tensor = normalized[np.newaxis, :, :, np.newaxis]
    
    # EEGNet expects (Batch, Channels, Samples, Kernels)
    assert input_tensor.shape == (1, 8, 250, 1)
