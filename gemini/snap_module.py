import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import screen_brightness_control as sbc
from pynput.mouse import Button, Controller
from math import hypot
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

mouse = Controller()
screen_width, screen_height = pyautogui.size()

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2
)
draw = mp.solutions.drawing_utils

# Audio Control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol, _ = volRange


def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    return np.abs(np.degrees(radians))


def get_distance(landmarks):
    if len(landmarks) < 2:
        return
    (x1, y1), (x2, y2) = landmarks[0], landmarks[1]
    return np.hypot(x2 - x1, y2 - y1)


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None


def move_mouse(index_finger_tip):
    if index_finger_tip:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x, y)


def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = get_distance([landmark_list[4], landmark_list[5]])

        # Move Mouse
        if thumb_index_dist < 50 and get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)

        # Left Click
        elif get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and thumb_index_dist > 50:
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Right Click
        elif get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and thumb_index_dist > 50:
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Screenshot
        elif get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and thumb_index_dist < 50:
            screenshot = pyautogui.screenshot()
            screenshot.save(f'screenshot_{np.random.randint(1, 1000)}.png')
            cv2.putText(frame, "Screenshot", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Scrolling
        elif get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 100:
            pyautogui.scroll(5)

        # Brightness Adjustment
        left_distance = get_distance([landmark_list[4], landmark_list[8]])
        brightness_level = np.interp(left_distance, [50, 220], [0, 100])
        sbc.set_brightness(int(brightness_level))

        # Volume Adjustment
        right_distance = get_distance([landmark_list[4], landmark_list[8]])
        volume_level = np.interp(right_distance, [50, 220], [minVol, maxVol])
        volume.SetMasterVolumeLevel(volume_level, None)


def process_frame(frame):
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    processed = hands.process(frameRGB)

    landmark_list = []
    if processed.multi_hand_landmarks:
        for handlm in processed.multi_hand_landmarks:
            draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)
            for lm in handlm.landmark:
                landmark_list.append((lm.x, lm.y))

    detect_gesture(frame, landmark_list, processed)
    return frame

def main():
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame = process_frame(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

