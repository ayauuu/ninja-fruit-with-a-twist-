import cv2
import numpy as np

class HandDetector:
    def __init__(self, smoothing=0.5):
        self.smoothing = smoothing  # 0 = no smoothing, closer to 1 = more smoothing/lag
        self.prev_x, self.prev_y = None, None

    def find_hand_position(self, frame):
        h, w, _ = frame.shape

        # Slight blur reduces per-frame noise in the mask
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # HSV range for bright orange marker
        lower_color = np.array([5, 150, 150])
        upper_color = np.array([25, 255, 255])

        mask = cv2.inRange(hsv, lower_color, upper_color)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        fingertip_pos = None

        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 800:  # raised threshold to reject small noise blobs
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Exponential smoothing to stabilize the point across frames
                    if self.prev_x is None:
                        smooth_x, smooth_y = cx, cy
                    else:
                        smooth_x = int(self.prev_x + (cx - self.prev_x) * (1 - self.smoothing))
                        smooth_y = int(self.prev_y + (cy - self.prev_y) * (1 - self.smoothing))

                    self.prev_x, self.prev_y = smooth_x, smooth_y
                    fingertip_pos = (smooth_x, smooth_y)

                    cv2.circle(frame, (smooth_x, smooth_y), 15, (0, 255, 0), cv2.FILLED)

        if fingertip_pos is None:
            # marker lost this frame — reset so next detection isn't smoothed toward a stale point
            self.prev_x, self.prev_y = None, None

        return frame, fingertip_pos