# FYP_Motion_Detection

https://youtu.be/0uSA3xyXlwM [Link to tutorial video]

An AI to play the Rock Paper Scissors game

## Requirements
- Python 3
- Keras
- Tensorflow
- OpenCV

## Set up instructions
1. Clone the repo.
```sh
$ git clone https://github.com/Aaminah2611/FYP_Motion_Detection.git
$ cd rock-paper-scissors
```

2. Install the dependencies
```sh
$ pip install -r requirements.txt
```
3. Edit source files

Navigate to:
```sh
venv / Lib / keras_squeezenet/__init__.py
```

change this line of code: 
```sh
from keras.applications.imagenet_utils import _obtain_input_shape
```

to this instead: 
```sh
from keras_applications.imagenet_utils import _obtain_input_shape
```

Comment out this import: 
```sh
# from keras.engine.topology import get_source_inputs
```

add this new import instead:
```sh
from keras.utils import get_source_inputs
```



4. Gather Images for each gesture (rock, paper and scissors and None):
In this example, we gather 200 images for the "rock" gesture
```sh
$ py gather_images.py rock 200
```

5. Train the model
```sh
$ py train.py
```

6. Test the model on some images
```sh
$ py test.py <path_to_test_image>
```

6. Play the game with your computer!
```sh
$ py play.py
```


