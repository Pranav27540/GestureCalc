import cv2
import mediapipe as mp
import numpy as np
import time
import sys

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Add a mapping from gesture symbol to label
GESTURE_LABELS = {
    '+': 'Addition',
    '-': 'Subtraction',
    '*': 'Multiplication',
    '/': 'Division',
    'sqrt': 'Square Root',
    '=': 'Equals',
    'del': 'Delete',
    'clear': 'Clear',
    'exit': 'Exit',
    'percent': 'Percentage',
}

def euclidean_distance(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def count_fingers(hand_landmarks, label):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if label == "Left":
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x else 0)

    # Other four fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

# Recognize gestures based on both hands
def detect_gesture(hand1_data, hand2_data):
    (hand1, label1), (hand2, label2) = hand1_data, hand2_data
    f1 = count_fingers(hand1, label1)
    f2 = count_fingers(hand2, label2)
    dist = euclidean_distance(hand1.landmark[8], hand2.landmark[8])  # index tips

    # Operator gestures
    if f1 == 1 and f2 == 1:
        if dist < 0.06:
            return "exit"
        return "+"
    elif (f1, f2) in [(1, 2), (2, 1)]:
        return "-"
    elif (f1, f2) in [(1, 3), (3, 1)]:
        return "*"
    elif (f1, f2) in [(1, 4), (4, 1)]:
        return "/"
    # Square root gesture: both hands showing only the pinky (1 finger each, but not index/thumb)
    elif (f1, f2) == (1, 1):
        # Check if both hands have only the pinky up (landmark 20)
        def only_pinky_up(hand_landmarks, label):
            tip_ids = [4, 8, 12, 16, 20]
            up = [
                hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y if i != 0 else (
                    hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x if label == "Left" else hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x
                )
                for i in range(5)
            ]
            return up == [0, 0, 0, 0, 1]
        if only_pinky_up(hand1, label1) and only_pinky_up(hand2, label2):
            return "sqrt"
    # Digit gestures (6–9)
    if (f1 == 5 and f2 in [1, 2, 3, 4]) or (f2 == 5 and f1 in [1, 2, 3, 4]):
        return str(5 + min(f1, f2))

    # Special gestures
    if f1 == 0 and f2 == 0:
        return "="
    if f1 == 2 and f2 == 2:
        # Check if both hands have only index and middle fingers up
        def is_peace_sign(hand_landmarks, label):
            tip_ids = [4, 8, 12, 16, 20]
            up = [
                hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y if i != 0 else (
                    hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x if label == "Left" else hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x
                )
                for i in range(5)
            ]
            return up == [0, 1, 1, 0, 0]
        if is_peace_sign(hand1, label1) and is_peace_sign(hand2, label2):
            return "percent"
    if f1 == 5 and f2 == 5:
        return "clear"
    
    return None

# Initialize webcam
if sys.platform == 'darwin':
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
else:
    cap = cv2.VideoCapture(0)
expression = ""
result = ""
last_update_time = 0
delay = 1.25
last_gesture_label = ""

while True:
    if not cap.isOpened():
        blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(blank_frame, "Camera not available or disconnected.", (30, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.putText(blank_frame, "Please check permissions or hardware.", (60, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.imshow("MathWave", blank_frame)
        key = cv2.waitKey(1000)
        if key == ord('q') or key == 27:
            break
        # Try to reinitialize the camera
        cap.release()
        if sys.platform == 'darwin':
            cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        else:
            cap = cv2.VideoCapture(0)
        continue
    success, frame = cap.read()
    if not success or frame is None:
        blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(blank_frame, "Camera not available or disconnected.", (30, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.putText(blank_frame, "Please check permissions or hardware.", (60, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.imshow("MathWave", blank_frame)
        key = cv2.waitKey(1000)
        if key == ord('q') or key == 27:
            break
        # Try to reinitialize the camera
        cap.release()
        if sys.platform == 'darwin':
            cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        else:
            cap = cv2.VideoCapture(0)
        continue
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    current_time = time.time()
    hand_data = []

    # Process hands
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_lm, hand_type in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = hand_type.classification[0].label
            hand_data.append((hand_lm, label))
            mp_drawing.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)

        # One hand for digits 0–5
        if len(hand_data) == 1:
            hand_lm, label = hand_data[0]
            count = count_fingers(hand_lm, label)
            if 0 <= count <= 5 and current_time - last_update_time > delay:
                expression += str(count)
                last_update_time = current_time

        # Two hands for gestures
        elif len(hand_data) == 2:
            gesture = detect_gesture(hand_data[0], hand_data[1])
            if gesture and current_time - last_update_time > delay:
                if gesture == "clear":
                    expression = ""
                    result = ""
                    last_gesture_label = GESTURE_LABELS.get(gesture, gesture)
                elif gesture == "del":
                    expression = expression[:-1]
                    last_gesture_label = GESTURE_LABELS.get(gesture, gesture)
                elif gesture == "=":
                    try:
                        result = str(eval(expression))
                    except:
                        result = "Error"
                    last_gesture_label = GESTURE_LABELS.get(gesture, gesture)
                elif gesture == "exit":
                    last_gesture_label = GESTURE_LABELS.get(gesture, gesture)
                    break
                elif gesture == "sqrt":
                    try:
                        val = eval(expression) if expression else 0
                        result = str(np.sqrt(val))
                        expression = f"sqrt({expression})"
                    except:
                        result = "Error"
                    last_gesture_label = GESTURE_LABELS.get(gesture, gesture)
                elif gesture == "percent":
                    try:
                        val = eval(expression) if expression else 0
                        result = str(val / 100)
                        expression = f"({expression})%"
                    except:
                        result = "Error"
                    last_gesture_label = GESTURE_LABELS.get(gesture, gesture)
                else:
                    expression += gesture
                    last_gesture_label = GESTURE_LABELS.get(gesture, gesture)
                last_update_time = current_time

    # Display on screen
    cv2.putText(frame, f"Expression: {expression}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, f"Result: {result}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    if last_gesture_label:
        cv2.putText(frame, f"Gesture: {last_gesture_label}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 128, 255), 2)

    cv2.imshow("MathWave", frame)
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break
    elif key == ord('c'):
        expression = ""
        result = ""

cap.release()
cv2.destroyAllWindows()
