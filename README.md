# GestureCalc -  A Real-Time Gesture-Based Calculator
GestureCalc is an innovative, real-time gesture-based calculator that leverages computer vision and machine learning to allow users to perform mathematical operations using only their hands and a webcam. Designed for accessibility, education, and futuristic human-computer interaction, GestureCalc transforms your webcam into a touchless math input device, recognizing hand gestures to build and solve math expressions live on screen.

**📚 Table of Contents**
Overview

●**Key Features**

●**How It Works**

●**Gesture Guide**

●**Technical Details**

●**Usage**

●**Troubleshooting**


**🔍 Overview**

GestureCalc is designed to make math input more natural, fun, and accessible. By using MediaPipe and OpenCV, it recognizes a variety of hand gestures through your webcam, translating them into numbers, operators, and commands. This project is ideal for:

Touchless interfaces (e.g., public kiosks, accessibility tools)
Educational demonstrations
Experimenting with computer vision and gesture recognition

**✨ Key Features**

Real-Time Gesture Recognition: Instantly detects and interprets hand gestures for numbers, operators, and special commands.
Touchless Math Input: Build and solve math expressions without touching your keyboard or mouse.
Robust Camera Handling: Special handling for macOS and error messages if the camera is unavailable or disconnected.
Live Feedback: See your gesture, current expression, and result on the screen in real time.
Cross-Platform: Works on macOS, Windows, and Linux (Python 3.10 required).
Extensible: Easily add new gestures or operations.

**⚙️ How It Works**
Hand Detection: Uses MediaPipe to detect and track hands in the webcam feed.

Gesture Recognition: Analyzes finger positions to recognize numbers (0–9), operators (+, -, *, /), and special commands (clear, equals, exit, etc.).
Expression Building: As you perform gestures, AirCalc builds a math expression.
Evaluation: When you signal 'equals', the expression is evaluated and the result is displayed.
Error Handling: If the camera is disconnected or unavailable, AirCalc displays a clear message and waits for reconnection.

**✋ Gesture Guide**

Numbers

0–5: Show 0–5 fingers on one hand.

6–9: Show 5 fingers on one hand and 1–4 on the other (6 = 5+1, 7 = 5+2, etc.).

Operators

->Addition (+): 1 finger up on each hand (index fingers), hands apart.
->Subtraction (−): 1 finger up on one hand, 2 on the other (or vice versa).
->Multiplication (×): 1 finger up on one hand, 3 on the other (or vice versa).
->Division (÷): 1 finger up on one hand, 4 on the other (or vice versa).
->Square Root (√): Both hands, only pinky finger up.
->Equals (=): Both hands, all fingers down (fists).
->Percentage (%): Both hands, only index and middle fingers up (peace sign).
->Clear: Both hands, all 5 fingers up.

Exit: 1 finger up on each hand, index fingertips close together.

Manual Controls

Clear: Press 'c' on the keyboard.
Exit: Press 'q' or 'Esc' on the keyboard.

**🔧 Technical Details**
Language: Python 3.10

**Libraries:**

**OpenCV** – Video capture and display

**MediaPipe** – Hand tracking

**Numpy** – Calculations

**Camera Handling**
On macOS, uses cv2.CAP_AVFOUNDATION for stable camera access.

If the camera is disconnected, AirCalc displays a message and waits for reconnection.

**Expression Evaluation**
Uses Python's eval() for basic math (with error handling for invalid input).


**▶️ Usage**

Make sure your webcam is connected and accessible.
Start the program and position your hands in front of the camera.
Use the gesture guide above to input numbers and operations.
The current expression, result, and last recognized gesture will be displayed on the video feed.
If the camera disconnects, follow the on-screen instructions to reconnect or exit.

**🧩 Troubleshooting**

Camera Not Detected:
Ensure your webcam is connected and not used by another application.
On macOS, grant camera access to Terminal/Python in System Preferences > Security & Privacy.

Dependency Issues:
Run pip install -r requirements.txt to ensure all dependencies are installed.

Gesture Not Recognized:
Ensure your hand is well-lit and fully visible to the camera.

Hold gestures steady for a moment to allow recognition.

Performance Issues:
Close other applications using the camera or heavy system resources.
