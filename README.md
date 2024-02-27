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

3. Gather Images for each gesture (rock, paper and scissors and None):
In this example, we gather 200 images for the "rock" gesture
```sh
$ py gather_images.py rock 200
```

4. Train the model
```sh
$ py train.py
```

5. Test the model on some images
```sh
$ py test.py <path_to_test_image>
```

6. Play the game with your computer!
```sh
$ py play.py
```


