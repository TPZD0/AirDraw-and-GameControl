import cv2
import numpy as np
import mediapipe as mp
import pyautogui  # Change this to PyDirectInput
import pydirectinput  # Import for direct input simulation

# Initialize MediaPipe Hands and Drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Function to identify which fingers are extended
def get_finger_states(hand_landmarks):
    # Fingers: 0 - Thumb, 1 - Index, 2 - Middle, 3 - Ring, 4 - Pinky
    finger_states = [0, 0, 0, 0, 0]
    
    # Thumb: Check if thumb is extended (special case, check between tip and MCP joint)
    if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
        finger_states[0] = 1
    
    # Check for other fingers (index, middle, ring, pinky)
    for i, tip in enumerate([8, 12, 16, 20]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[i + 1] = 1
    
    return finger_states

# Initialize variables for controlling the game
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the frame and detect hands
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the finger states (which fingers are extended)
                finger_states = get_finger_states(hand_landmarks)
                
                # Display the finger states as an array on the frame
                finger_text = str(finger_states)
                cv2.putText(frame, f"Fingers: {finger_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Simulate key presses based on finger states and show actions on screen
                action_text = ""
                
                # Move forward (Index and Middle fingers up)
                if finger_states == [0, 1, 1, 0, 0]:
                    pydirectinput.press('w')
                    action_text = "Pressing W (Move Forward)"
                
                # Move down (Index, Middle, and Ring fingers up)
                elif finger_states == [0, 1, 1, 1, 0]:
                    pydirectinput.press('s')
                    action_text = "Pressing S (Move Down)"
                
                # Move left (Pinky finger up)
                elif finger_states == [0, 0, 0, 0, 1]:
                    pydirectinput.press('a')
                    action_text = "Pressing A (Move Left)"
                
                # Move right (Index and Ring fingers up)
                elif finger_states == [1, 0, 0, 0, 0]:
                    pydirectinput.press('d')
                    action_text = "Pressing D (Move Right)"

                
                else:
                    action_text = "No key pressed"

                # Display the action being taken on the frame
                cv2.putText(frame, action_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Game Control - Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

# 
