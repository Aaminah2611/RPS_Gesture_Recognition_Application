desc = '''Script to gather data images with a particular label.

Usage: python gather_images.py <label_name> <num_samples>

The script will collect <num_samples> number of images and store them
in its own directory.

Only the portion of the image within the box displayed
will be captured and stored.

Press 'a' to start/pause the image collecting process.
Press 'q' to quit.

'''

import cv2
import os
import sys
import time
import uuid

try:
    label_name = sys.argv[1]
    num_samples = int(sys.argv[2])
except:
    print("Arguments missing.")
    print(desc)
    exit(-1)

IMG_SAVE_PATH = '../image_data'
IMG_CLASS_PATH = os.path.join(
    'C:\\Users\Aamin\\OneDrive - Aston University\\University\\Term 2\\IP\\Submissions\\game\\sample images', label_name)

try:
    os.mkdir(IMG_SAVE_PATH)
except FileExistsError:
    pass
try:
    os.mkdir(IMG_CLASS_PATH)
except FileExistsError:
    print("{} directory already exists.".format(IMG_CLASS_PATH))
    print("All images gathered will be saved along with existing items in this folder")

cap = cv2.VideoCapture(0)

# Flip the frame horizontally

# Set the resolution to 640x480 (you can adjust this to your desired resolution)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

start = False
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    if count == num_samples:
        break

    frame = cv2.flip(frame, 1)

    # Rectangle for user to play (left side)
    cv2.rectangle(frame, (100, 100), (400, 400), (255, 255, 255), 2)

    if start:
        roi = frame[100:400, 100:400]
        unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
        save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(unique_id))
        cv2.imwrite(save_path, roi)
        count += 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Collecting {}".format(count),
                (5, 50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Collecting images", frame)

    k = cv2.waitKey(10)
    if k == ord('a'):
        start = not start

    if k == ord('q') or count == num_samples:
        break

print("\n{} image(s) saved to {}".format(count, IMG_CLASS_PATH))
cap.release()
cv2.destroyAllWindows()

