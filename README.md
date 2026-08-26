# Fruit Ninja Hand Controller

Control the browser game [Fruit Ninja](https://poki.com/en/g/fruit-ninja) using a colored marker (e.g. a highlighter) tracked through your webcam, instead of a mouse.

## How it works

1. **`detector.py`** captures webcam frames and uses OpenCV color detection (HSV thresholding) to locate a bright orange/yellow marker in the frame. It returns the marker's screen position each frame, smoothed to reduce jitter.
2. **`main.py`** maps that position to actual screen coordinates and uses `pyautogui` to move the mouse and hold a click-drag, simulating a "slice" gesture as you move the marker.

## Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy
- PyAutoGUI

Install dependencies:

```bash
pip install opencv-python numpy pyautogui
```

## Setup

1. Get a brightly colored marker (orange/yellow works best with the default HSV range in `detector.py`).
2. Open [Fruit Ninja on Poki](https://poki.com/en/g/fruit-ninja) in your browser.
3. Run the controller:

```bash
python main.py
```

4. **Calibration**: when prompted in the terminal, hover your mouse over the top-left corner of the game canvas and press Enter, then do the same for the bottom-right corner. This tells the script exactly where the game area is on your screen.
5. A camera preview window will open. Hold your marker up to the camera and move it — the game cursor will follow, and a virtual click stays "held down" as you move, so passing the marker over fruit slices them.
6. Press `q` in the camera window to quit.

## Tips

- Keep the camera preview window away from the game canvas so it doesn't block your view or the mouse mapping.
- For best tracking, use good, even lighting and a marker color that contrasts with your background and skin tone.
- If tracking is unstable or grabs the wrong object, adjust the HSV range (`lower_color` / `upper_color`) in `detector.py` to match your specific marker.

## Files

| File | Purpose |
|---|---|
| `main.py` | Runs the calibration, capture loop, and mouse control |
| `detector.py` | Detects the marker's position in each camera frame |

## Known limitations

- Color-based tracking can be sensitive to lighting changes.
- Calibration must be redone if you move or resize the browser window.
