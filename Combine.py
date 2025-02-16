import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import pydirectinput

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Get screen size for scaling mouse movement
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

# Initialize camera
cap = cv2.VideoCapture(0)

# Set border width in pixels
border_width = 50  

def get_finger_states(hand_landmarks, is_right_hand):
    """Detects which fingers are extended."""
    finger_states = [0, 0, 0, 0, 0]  # [Thumb, Index, Middle, Ring, Pinky]
    
    # Thumb: Adjust logic based on hand type
    if is_right_hand:
        finger_states[0] = 1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0
    else:
        finger_states[0] = 1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0
    
    # Check for other fingers (Index, Middle, Ring, Pinky)
    for i, tip in enumerate([8, 12, 16, 20]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[i + 1] = 1
    
    return finger_states

move_mouse = False  # Track whether mouse movement is enabled

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally to mirror the image
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert frame to RGB for processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    right_hand_action = "No Action"
    left_hand_action = "No Action"

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[i].classification[0].label
            is_right_hand = handedness == "Right"

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            finger_states = get_finger_states(hand_landmarks, is_right_hand)

            if is_right_hand:
                # Right hand controls the mouse
                index_tip = hand_landmarks.landmark[8]
                x, y = int(index_tip.x * w), int(index_tip.y * h)
                screen_x = int((x - border_width) * screen_width / (w - 2 * border_width))
                screen_y = int((y - border_width) * screen_height / (h - 2 * border_width))

                # Perform actions based on finger states
                if finger_states == [0, 1, 1, 0, 0]:  
                    move_mouse = True
                    right_hand_action = "Moving Mouse"
                else:
                    move_mouse = False  # Stop moving when different gesture is detected

                if move_mouse:
                    pyautogui.moveTo(screen_x, screen_y)

                # Mouse click actions
                if finger_states == [1, 0, 1, 0, 0]:  
                    pyautogui.click()
                    right_hand_action = "Left Click"
                elif finger_states == [1, 1, 0, 0, 0]:  
                    pyautogui.rightClick()
                    right_hand_action = "Right Click"

            else:
                # Left hand controls the game
                if finger_states == [0, 1, 1, 0, 0]:
                    pydirectinput.press('w')
                    left_hand_action = "Pressing W (Move Forward)"
                elif finger_states == [0, 1, 1, 1, 0]:
                    pydirectinput.press('s')
                    left_hand_action = "Pressing S (Move Down)"
                elif finger_states == [0, 0, 0, 0, 1]:
                    pydirectinput.press('a')
                    left_hand_action = "Pressing A (Move Left)"
                elif finger_states == [1, 0, 0, 0, 0]:
                    pydirectinput.press('d')
                    left_hand_action = "Pressing D (Move Right)"
                elif finger_states == [0, 0, 0, 0, 0]:
                    pydirectinput.press('space')
                    left_hand_action = "Pressing Space (Jump)"
                elif finger_states == [1, 1, 1, 0, 1]:
                    left_hand_action = "Quitting Program"
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

    # Display action text on screen
    cv2.putText(frame, f"Right Hand: {right_hand_action}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Left Hand: {left_hand_action}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show frame
    cv2.imshow('Hand Tracking - Mouse & Game Control', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
