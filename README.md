# FYP_Motion_Detection


## Requirements
- Python 3
- Keras
- Tensorflow
- OpenCV

___________________________________________________

## Installation Guide

1. Clone the repo:
```sh
$ git clone https://github.com/Aaminah2611/FYP_Motion_Detection.git
```

2. Navigate to the directory:
```sh
$ cd rock-paper-scissors
```

4. Install dependencies
```sh
$ pip install -r requirements.txt
```

6. Edit source files

6.1 Navigate to:
```sh
venv / Lib / keras_squeezenet/squeezenet.py
```

Error:
```sh
ImportError: cannot import name '_obtain_input_shape' from 'keras.applications.imagenet_utils
```

change this line of code: 
```sh
from keras.applications.imagenet_utils import _obtain_input_shape
```

[Fix] to this instead: 
```sh
from keras_applications.imagenet_utils import _obtain_input_shape
```

6.2 Error:
```sh
ImportError: cannot import name 'warnings' from 'keras.layers'
```

Fix: Remove the word 'warnings' from the following line of code:
```sh
from keras.layers import Input, Convolution2D, MaxPooling2D, Activation, concatenate, Dropout, warnings
```

6.3 remove this if statement:
```sh
        if K.image_data_format() == 'channels_first':

            if K.backend() == 'tensorflow':
                warnings.warn('You are using the TensorFlow backend, yet you '
                              'are using the Theano '
                              'image data format convention '
                              '(`image_data_format="channels_first"`). '
                              'For best performance, set '
                              '`image_data_format="channels_last"` in '
                              'your Keras config '
                              'at ~/.keras/keras.json.')
```
6.4 Error:
```sh
ModuleNotFoundError: No module named 'keras.engine.topology'
```

Comment out this import: 
```sh
# from keras.engine.topology import get_source_inputs
```

[Fix] add this new import instead:
```sh
from keras.utils import get_source_inputs
```

Ensure machine learning model is present.
Model should be titled: ```Rock-Paper-Scissors.keras```, and should be in the ```Keras``` directory

Play Singeplayer mode:
```sh
$ py singleplayer.py
```

Play Multiplayer mode:
```sh
$ py multiplayer.py
```
