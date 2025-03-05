# Gesture Recognition Rock-Paper-Scissors Game

## Project Overview
This project develops an interactive Rock-Paper-Scissors game utilizing advanced gesture recognition technologies. The application uses machine learning and computer vision to enable players to play the classic game through hand gesture detection via camera input.

## Key Features
- Real-time gesture recognition using Convolutional Neural Networks (CNNs)
- Single-player and multiplayer game modes
- Web-based application with responsive interface
- Database integration for game statistics

## Technologies Used

### Backend
- **Language**: Python
- **Web Framework**: Flask (chosen for lightweight nature and flexibility)
- **Machine Learning**:
  - TensorFlow
  - Keras (with SqueezeNet architecture)
- **Computer Vision**: OpenCV

### Database
- **Database Management System**: MySQL
- **ORM**: SQLAlchemy
- **Database Features**:
  - Game state tracking
  - Player statistics storage
  - Potential for future leaderboard implementation

### Frontend
- HTML
- Bootstrap
- JavaScript

## Web Application
The project includes a fully-developed web application framework using Flask, designed to provide a seamless and interactive user experience. The web interface offers:
- Dynamic route handling
- Real-time game state rendering
- Responsive design using HTML and Bootstrap
- Integrated OpenCV video processing

![image](https://github.com/user-attachments/assets/8cf8d74c-3749-4bd5-80ce-4298b9464ade)


## Machine Learning Model Details
- **Model Architecture**: Convolutional Neural Network (CNN)
- **Framework**: Keras with SqueezeNet
- **Training Dataset**: 
  - Four labels: rock, paper, scissors, none
  - Diverse images covering variations in:
    - Lighting conditions
    - Sizes
    - Skin tones
- **Data Augmentation**: 
  - Used ImageDataGenerator
  - Augmentation techniques: rotation, zoom

## Game Modes
1. **Single-player**: 
   - Player competes against computer

![image](https://github.com/user-attachments/assets/1c261d66-36e5-4cdf-bfb5-c4d2d3ba778f)


2. **Multiplayer**: 
   - Two players compete using camera inputs
   - Real-time gesture recognition
   - Winner calculated dynamically

![image](https://github.com/user-attachments/assets/d204577c-ad3b-49da-b802-14649d179bb4)


## Future Enhancements
- Leaderboard integration
- Settings menu
- In-game chat feature
- Improved UI/UX

___________________________________________

## Requirements
- Python 3
- Keras
- TensorFlow
- OpenCV
- MySQL

## Installation Guide
1. Clone the repository:
```sh
$ git clone https://github.com/Aaminah2611/FYP_Motion_Detection.git
```

2. Navigate to the project directory:
```sh
$ cd rock-paper-scissors
```

3. Install dependencies:
```sh
$ pip install -r requirements.txt
```

4. Prepare Machine Learning Model:
   - Ensure the machine learning model is present
   - Model should be titled: `Rock-Paper-Scissors.keras`
   - Place the model in the `Keras` directory

5. Running the Application:
   - Single-player mode:
     ```sh
     $ py singleplayer.py
     ```
   - Multiplayer mode:
     ```sh
     $ py multiplayer.py
     ```
