import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Get screen size for scaling mouse movement
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

# Initialize camera
cap = cv2.VideoCapture(0)

# Set border width in pixels
border_width = 50  # Adjust for your camera resolution

# Flag to control mouse movement
move_mouse = False


def get_finger_states(hand_landmarks, handedness):
    """Detects which fingers are extended."""
    finger_states = [0, 0, 0, 0, 0]  # [Thumb, Index, Middle, Ring, Pinky]
    
    is_right_hand = handedness.classification[0].label == "Right"

    # Thumb: Adjust logic based on hand type
    if is_right_hand:
        finger_states[0] = 1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0
    else:  # Left hand
        finger_states[0] = 1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0
    
    # Check for other fingers (Index, Middle, Ring, Pinky)
    for i, tip in enumerate([8, 12, 16, 20]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[i + 1] = 1
    
    return finger_states


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally to mirror the image
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Define borders for mouse control
    border_left, border_top = border_width, border_width
    border_right, border_bottom = w - border_width, h - border_width

    # Draw the border (for visualization)
    cv2.rectangle(frame, (border_left, border_top), (border_right, border_bottom), (0, 255, 0), 2)

    # Convert frame to RGB for processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Assume no gesture detected
    move_mouse = False
    action_text = "No action"

    # Check if a hand is detected
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[i]  # Detect if it's right or left hand

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the index finger tip position
            index_tip = hand_landmarks.landmark[8]
            x, y = int(index_tip.x * w), int(index_tip.y * h)

            # Map the finger's position inside the border to the screen
            screen_x = int((x - border_left) * screen_width / (border_right - border_left)) if border_left <= x <= border_right else (screen_width - 1 if x > border_right else 0)
            screen_y = int((y - border_top) * screen_height / (border_bottom - border_top)) if border_top <= y <= border_bottom else (screen_height - 1 if y > border_bottom else 0)

            # Detect finger states
            finger_states = get_finger_states(hand_landmarks, handedness)

            # Display finger states on screen
            cv2.putText(frame, f"Fingers: {finger_states}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Perform actions based on finger states
            if finger_states == [0, 1, 1, 0, 0]:  # Move the mouse (Index & Middle Extended)
                move_mouse = True
                action_text = "Moving Mouse"
            elif finger_states == [1, 1, 1, 0, 0]:  # Stop Moving Mouse (Thumb, Index, Middle Extended)
                move_mouse = False
                action_text = "Stopping Mouse"
            elif finger_states == [1, 0, 1, 0, 0]:  # Left Click (Thumb & Middle Extended)
                pyautogui.click()
                action_text = "Left Click"
            elif finger_states == [1, 1, 0, 0, 0]:  # Right Click (Thumb & Index Extended)
                pyautogui.rightClick()
                action_text = "Right Click"

            elif finger_states == [1, 1, 1, 0, 1]:  # Right Click (Thumb & Index Extended)
                cap.release()
                cv2.destroyAllWindows()


            # Move mouse only when move_mouse is True
            if move_mouse:
                pyautogui.moveTo(screen_x, screen_y)

    # Display action text
    cv2.putText(frame, action_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show frame
    cv2.imshow('Hand Tracking with Border', frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
