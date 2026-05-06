# Signal Processing Theory: The Cerebrum Pipeline

## 1. Temporal Filtering (Butterworth)
We utilize a **4th-order Butterworth Bandpass Filter** (1-40Hz). 
- **Rationale:** Butterworth filters provide a maximally flat frequency response in the passband, essential for preserving the relative power of Mu and Beta rhythms.
- **Implementation:** `scipy.signal.butter` + `lfilter`.

## 2. Spatial Filtering (Common Spatial Patterns - CSP)
CSP is our primary algorithm for Motor Imagery (MI) feature extraction.
- **The Math:** CSP finds spatial filters that maximize the variance of the signal for one class (e.g., Left Hand) while minimizing it for the other (Right Hand).
- **Result:** It transforms the 8-channel EEG into a new coordinate system where the most discriminative information is concentrated in the first and last components.

## 3. The Neural Decoder (EEGNet)
EEGNet is a compact Convolutional Neural Network (CNN) designed for EEG.
- **Depthwise Convolutions:** Used to learn spatial filters (similar to CSP) for each temporal filter.
- **Separable Convolutions:** Used to learn temporal summaries of each feature map.
- **Efficiency:** By using fewer parameters than traditional CNNs, EEGNet prevents overfitting on small, noisy neuro-datasets.

## 4. Real-time Inference Engine
The pipeline is optimized via **TensorFlow Lite Quantization**. By converting the model to 8-bit integer precision, we reduce inference latency on the Raspberry Pi 5 to <4ms, enabling high-bandwidth, real-time BCI control.
