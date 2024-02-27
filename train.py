import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
from tensorflow.keras.layers import Layer, InputSpec
import tensorflow as tf
import os
import random
from keras.preprocessing.image import ImageDataGenerator


IMG_SAVE_PATH = 'image_data'

CLASS_MAP = {
    "rock": 0,
    "paper": 1,
    "scissors": 2,
    "none": 3
}

NUM_CLASSES = len(CLASS_MAP)

def mapper(val):
    return CLASS_MAP[val]

def get_model():
    model = Sequential([
        SqueezeNet(input_shape=(227, 227, 3), include_top=False),
        Dropout(0.1),
        Convolution2D(NUM_CLASSES, (1, 1), padding='valid'),
        Activation('relu'),
        GlobalAveragePooling2D(),
        Activation('softmax')
    ])
    return model

# load images from the directory
dataset = []
for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join('C:\\Users\\Aamin\\OneDrive\\Desktop\\University\\Term 2\\IP\\Submissions\\game\\sample images',directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        # to make sure no hidden files get in our way
        if item.startswith("."):
            continue
        img = cv2.imread(os.path.join(path, item))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        dataset.append([img, directory])

print("Number of samples in dataset:", len(dataset))

# Split the dataset into training and validation sets
random.shuffle(dataset)  # Shuffle the dataset
split_ratio = 0.8  # Define the ratio of training to validation data
split_index = int(len(dataset) * split_ratio)
train_data = dataset[:split_index]
val_data = dataset[split_index:]

# Extract data and labels for training
train_images = np.array([sample[0] for sample in train_data])
train_labels = to_categorical([mapper(sample[1]) for sample in train_data])

# Extract data and labels for validation
val_images = np.array([sample[0] for sample in val_data])
val_labels = to_categorical([mapper(sample[1]) for sample in val_data])

# Create an instance of ImageDataGenerator with desired augmentation parameters
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Generate augmented data batches from your existing dataset
batch_size = 200 # Set batch size equal to the number of training samples
augmented_train_generator = datagen.flow(train_images, train_labels, batch_size=batch_size)

# Define and compile the model
model = get_model()
model.compile(
    optimizer=Adam(learning_rate=0.00004),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model using the augmented data batches
epochs = 25
history = model.fit(augmented_train_generator,
                    steps_per_epoch=len(train_images) // batch_size,
                    epochs=epochs,
                    validation_data=(val_images, val_labels))

# Save the model
model.save("rock-paper-scissors-model.keras")
