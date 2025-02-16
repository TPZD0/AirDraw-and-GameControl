import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Get screen size for scaling mouse movement
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

# Initialize camera
cap = cv2.VideoCapture(0)

# Set border width in pixels (e.g., 1-2 cm depending on camera resolution)
border_width = 50  # Approximate 1-2 cm for most webcams (you can adjust this)

    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally to mirror the image
    frame = cv2.flip(frame, 1)

    # Get frame dimensions
    h, w, _ = frame.shape

    # Define the region inside the border for the mouse control (excluding 1-2 cm borders)
    border_left = border_width
    border_top = border_width
    border_right = w - border_width
    border_bottom = h - border_width

    # Draw the border (optional, for visualization)
    cv2.rectangle(frame, (border_left, border_top), (border_right, border_bottom), (0, 255, 0), 2)

    # Convert the frame to RGB for hand tracking
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get the hand landmarks
    results = hands.process(frame_rgb)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Draw the hand landmarks on the frame
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the index finger tip (Landmark 8)
            index_finger_tip = landmarks.landmark[8]

            # Convert the camera position to frame position
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)

            # Scale the mouse movement to the screen size
            # Map the finger's position inside the border to the screen, ensuring the mouse reaches screen edges
            screen_x = int((x - border_left) * screen_width / (border_right - border_left)) if border_left <= x <= border_right else (screen_width - 1 if x > border_right else 0)
            screen_y = int((y - border_top) * screen_height / (border_bottom - border_top)) if border_top <= y <= border_bottom else (screen_height - 1 if y > border_bottom else 0)

            # Move the mouse to the position of the index finger
            pyautogui.moveTo(screen_x, screen_y)

    # Display the frame
    cv2.imshow('Hand Tracking with Border', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()