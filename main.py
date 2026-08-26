import cv2
import numpy as np
import pyautogui
from detector import HandDetector

# Safety / performance settings
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0  # remove default delay between pyautogui calls

# Screen resolution (used to map camera coords -> screen coords)
screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)
detector = HandDetector()

print("Controller Active!")
print("Show your marker in front of the camera. Press 'q' in the camera window to quit.")

is_down = False
prev_x, prev_y = None, None

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    frame, fingertip = detector.find_hand_position(frame)

    if fingertip:
        cx, cy = fingertip

        # Map camera coordinates to full screen coordinates
        screen_x = np.interp(cx, [0, w], [0, screen_width])
        screen_y = np.interp(cy, [0, h], [0, screen_height])

        # Start holding the button down the first time we see the marker
        if not is_down:
            pyautogui.mouseDown()
            is_down = True
            prev_x, prev_y = screen_x, screen_y

        # Interpolate a few steps between the last and current position
        # so fast movement doesn't skip over fruit hitboxes
        steps = 5
        for i in range(1, steps + 1):
            ix = prev_x + (screen_x - prev_x) * i / steps
            iy = prev_y + (screen_y - prev_y) * i / steps
            pyautogui.moveTo(ix, iy, _pause=False)

        prev_x, prev_y = screen_x, screen_y

    else:
        # Marker lost — release so we don't drag a phantom slice around
        if is_down:
            pyautogui.mouseUp()
            is_down = False
            prev_x, prev_y = None, None

    cv2.imshow("Fruit Ninja Hand Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if is_down:
    pyautogui.mouseUp()

cap.release()
cv2.destroyAllWindows()