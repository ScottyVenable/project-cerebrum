import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelStandardScaler
from model import EEGNet # Importing our existing model architecture

# Mock Data Generator for Demonstration
# In production, use mne.io.read_raw_xdf to load recorded LSL data.
def load_and_preprocess_data():
    """
    Loads recorded Motor Imagery data and applies spatial/temporal filters.
    """
    print("[AI] Loading recorded neuro-data...")
    # Simulated 8-channel EEG at 250Hz, 100 trials, 2s windows
    X = np.random.randn(100, 8, 250, 1).astype(np.float32)
    y = np.random.randint(0, 2, 100) # Binary: Left vs Right
    return train_test_split(X, y, test_size=0.2)

def train_cerebrum_model():
    """
    Trains the EEGNet model on processed neural signals.
    """
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    
    print("[AI] Initializing EEGNet training...")
    model = EEGNet(nb_classes=2, Chans=8, Samples=250)
    
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])
    
    # Early stopping to prevent overfitting on neural noise
    callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    
    history = model.fit(X_train, y_train, 
                        epochs=50, 
                        validation_data=(X_test, y_test),
                        callbacks=[callback],
                        verbose=1)
    
    # Save the final weights
    model.save('/root/Coding/projects/project-cerebrum/ai_models/cerebrum_v1.h5')
    print("[AI] Training complete. Model saved.")
    
    # Export for Raspberry Pi optimization
    from model import export_to_tflite
    export_to_tflite(model, "/root/Coding/projects/project-cerebrum/ai_models/eegnet_quantized.tflite")

if __name__ == "__main__":
    train_cerebrum_model()
