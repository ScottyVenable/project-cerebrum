import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, DepthwiseConv2D, \
    Activation, AveragePooling2D, SeparableConv2D, Flatten, Dense, SpatialDropout2D
from tensorflow.keras.constraints import max_norm

def EEGNet(nb_classes, Chans=8, Samples=250, dropoutRate=0.5, kernLength=64, F1=8, D=2, F2=16, norm_rate=0.25):
    """ 
    EEGNet implementation for BCI on Raspberry Pi.
    Configured by default for 8 channels and 1-second windows at 250Hz.
    """
    input1 = Input(shape=(Chans, Samples, 1))

    # Block 1: Temporal + Spatial Convolution
    block1 = Conv2D(F1, (1, kernLength), padding='same', use_bias=False)(input1)
    block1 = BatchNormalization()(block1)
    block1 = DepthwiseConv2D((Chans, 1), use_bias=False, depth_multiplier=D,
                             depthwise_constraint=max_norm(1.))(block1)
    block1 = BatchNormalization()(block1)
    block1 = Activation('elu')(block1)
    block1 = AveragePooling2D((1, 4))(block1)
    block1 = SpatialDropout2D(dropoutRate)(block1)

    # Block 2: Separable Convolution
    block2 = SeparableConv2D(F2, (1, 16), use_bias=False, padding='same')(block1)
    block2 = BatchNormalization()(block2)
    block2 = Activation('elu')(block2)
    block2 = AveragePooling2D((1, 8))(block2)
    block2 = SpatialDropout2D(dropoutRate)(block2)

    flatten = Flatten(name='flatten')(block2)
    dense = Dense(nb_classes, name='dense', kernel_constraint=max_norm(norm_rate))(flatten)
    softmax = Activation('softmax', name='softmax')(dense)

    return Model(inputs=input1, outputs=softmax)

def export_to_tflite(model, filename="/root/Coding/projects/project-cerebrum/ai_models/eegnet_quantized.tflite"):
    """
    Converts and saves the Keras model to a quantized TFLite format for Raspberry Pi.
    """
    print(f"[AI] Converting model to TFLite: {filename}")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    
    with open(filename, 'wb') as f:
        f.write(tflite_model)
    print("[AI] Export complete.")

if __name__ == "__main__":
    # Test model initialization
    try:
        model = EEGNet(nb_classes=4)
        model.summary()
        # export_to_tflite(model) # Uncomment to export when running locally
        print("\n[AI] EEGNet architecture initialized successfully.")
    except Exception as e:
        print(f"\n[AI] Error: {e}")
