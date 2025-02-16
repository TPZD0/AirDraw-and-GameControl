import cv2
import numpy as np
import mediapipe as mp
import pydirectinput  # Import for direct input simulation

# Initialize MediaPipe Hands and Drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

def get_finger_states(hand_landmarks):
    finger_states = [0, 0, 0, 0, 0]
    
    # Thumb
    if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
        finger_states[0] = 1
    
    # Other fingers
    for i, tip in enumerate([8, 12, 16, 20]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[i + 1] = 1
    
    return finger_states

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_states = get_finger_states(hand_landmarks)
                
                finger_text = str(finger_states)
                cv2.putText(frame, f"Fingers: {finger_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                action_text = ""
                
                if finger_states == [0, 1, 1, 0, 0]:
                    pydirectinput.press('w')
                    action_text = "Pressing W (Move Forward)"
                elif finger_states == [0, 1, 1, 1, 0]:
                    pydirectinput.press('s')
                    action_text = "Pressing S (Move Down)"
                elif finger_states == [0, 0, 0, 0, 1]:
                    pydirectinput.press('a')
                    action_text = "Pressing A (Move Left)"
                elif finger_states == [1, 0, 0, 0, 0]:
                    pydirectinput.press('d')
                    action_text = "Pressing D (Move Right)"
                elif finger_states == [0, 0, 0, 0, 0]:
                    pydirectinput.press('space')
                    action_text = "Pressing Space (Jump)"
                elif finger_states == [1, 1, 1, 0, 1]:
                    action_text = "Quitting Program"
                    cv2.putText(frame, "Exiting...", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow('Game Control - Hand Tracking', frame)
                    cv2.waitKey(1000)
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()
                    ddd
                else:
                    action_text = "No key pressed"

                cv2.putText(frame, action_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Game Control - Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()