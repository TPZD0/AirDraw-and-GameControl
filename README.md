# Hand Gesture Control Programs

## 1. Hand Tracking Mouse Control

### Description
This program uses OpenCV, MediaPipe, and PyAutoGUI to track hand movements and control the mouse using specific hand gestures. The camera detects a single hand and maps the index finger position to the screen for cursor control. It also supports left-click, right-click, and toggling mouse movement using different gestures.

### Requirements
- Python 3.x
- OpenCV (`cv2`)
- MediaPipe
- PyAutoGUI

### Installation

pip install opencv-python mediapipe pyautogui

### Controls
| Hand Gesture                | Action              |
|-----------------------------|---------------------|
| Index & Middle Extended     | Move Mouse         |
| Thumb, Index & Middle Extended | Stop Mouse Movement |
| Thumb & Middle Extended     | Left Click         |
| Thumb & Index Extended      | Right Click        |
| Thumb, Index, Middle, and Pinky Extended | Exit Program |

### Usage
Run the script:
```sh
python hand_mouse_control.py
```
Press 'q' to quit.

---

## 2. Hand Gesture-Based Game Control

### Description
This program uses OpenCV, MediaPipe, and PyDirectInput to control keyboard inputs using hand gestures. The camera tracks hand gestures and triggers corresponding game controls, allowing movement and actions based on finger positioning.

### Requirements
- Python 3.x
- OpenCV (`cv2`)
- MediaPipe
- PyDirectInput


pip install opencv-python mediapipe pydirectinput


### Controls
| Hand Gesture            | Action              |
|-------------------------|---------------------|
| Index & Middle Extended | Press 'W' (Move Forward) |
| Index, Middle & Ring Extended | Press 'S' (Move Backward) |
| Pinky Extended         | Press 'A' (Move Left) |
| Thumb Extended         | Press 'D' (Move Right) |
| No Fingers Extended    | Press 'Space' (Jump) |
| Thumb, Index, Middle & Pinky Extended | Exit Program |

### Usage
Run the script:
```sh
python hand_game_control.py
```
Press 'Esc' to quit.

