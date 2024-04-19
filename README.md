# FYP_Motion_Detection

https://youtu.be/0uSA3xyXlwM [Link to tutorial video]

An AI to play the Rock Paper Scissors game

## Requirements
- Python 3
- Keras
- Tensorflow
- OpenCV

___________________________________________________

## Set up instructions
1. Clone the repo.
```sh
$ git clone https://github.com/Aaminah2611/FYP_Motion_Detection.git
$ cd rock-paper-scissors
```
_____________________________________________________

2. Install the dependencies
```sh
$ pip install -r requirements.txt
```

___________________________________________________

3. Edit source files

Navigate to:
```sh
venv / Lib / keras_squeezenet/squeezenet.py
```

In order to fix the following error complete step 3.1 below:

```sh
ImportError: cannot import name '_obtain_input_shape' from 'keras.applications.imagenet_utils
```

3.1. change this line of code: 
```sh
from keras.applications.imagenet_utils import _obtain_input_shape
```

to this instead: 
```sh
from keras_applications.imagenet_utils import _obtain_input_shape
```
//

In order to fix the following error complete step 3.2 & 3.3 below:

```sh
ImportError: cannot import name 'warnings' from 'keras.layers'
```

3.2. Remove the word 'warnings' from the following line of code:
```sh
from keras.layers import Input, Convolution2D, MaxPooling2D, Activation, concatenate, Dropout, warnings
```

3.3. remove this if statement:
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

//

In order to fix the following error complete step 3.4 below:

```sh
ModuleNotFoundError: No module named 'keras.engine.topology'
```

3.4. Comment out this import: 
```sh
# from keras.engine.topology import get_source_inputs
```

add this new import instead:
```sh
from keras.utils import get_source_inputs
```

__________________________________________________

4. Gather Images for each gesture (rock, paper and scissors and None):
In this example, we gather 200 images for the "rock" gesture
```sh
$ py gather_images.py rock 200
```
___________________________________________________
5. Train the model
```sh
$ py train.py
```
__________________________________________________

6. Test the model on some images
```sh
$ py test.py <path_to_test_image>
```
____________________________________________________

7. Play the game with your computer!
```sh
$ py singleplayer.py
```


