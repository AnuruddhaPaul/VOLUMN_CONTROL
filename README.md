# Volume Gesture Control

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

AI Volume Gesture Control is a computer vision-based system that allows users to control their computer's volume using hand gestures captured by a webcam. This project leverages **MediaPipe** for hand tracking and **pycaw** for volume control.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Gesture Controls](#gesture-controls)
- [Code Explanation](#code-explanation)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

This project implements volume control through hand gestures. Using your webcam, you can:

- **Adjust system volume** by changing the distance between your thumb and index finger.
- **Visualize the gesture** with connecting lines and circles at fingertips.
- **Exit the program** by pressing the `q` key.

---

## Requirements

Ensure you have the following installed:

- Python 3.6+
- OpenCV
- NumPy
- MediaPipe
- pycaw (Python Core Audio Windows Library)
- comtypes
- A working webcam

---

## Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/ai-volume-gesture.git
cd ai-volume-gesture
```

Install the required dependencies:

```bash
pip install opencv-python numpy mediapipe pycaw comtypes
```

---

## Usage

Run the main script:

```bash
python VOLUMN_GESTURE.py
```

---

## Gesture Controls

| Gesture | Action |
|---------------------------|------------------------|
| Thumb and index finger close | Lower volume |
| Thumb and index finger far apart | Increase volume |
| Press 'q' key | Exit program |

---

## Code Explanation

### `VOLUMN_GESTURE.py`

This script contains the main logic for hand gesture-based volume control.

- **Initialization and Setup:**

```python
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
minvol, maxvol, _ = volume.GetVolumeRange()
```

- Connects to the system's audio endpoint.
- Gets volume range for mapping.

- **Main Loop Features:**

  - **Hand Detection:**

  ```python
  frame = detector.findHands(frame)
  lmList = detector.findPosition(frame, draw=False)
  ```

  - **Distance Calculation:**

  ```python
  x1, y1 = lmList[4][1], lmList[4][2]  # Thumb
  x2, y2 = lmList[8][1], lmList[8][2]  # Index finger
  length = math.hypot(x2-x1, y2-y1)
  ```

  - **Volume Control:**

  ```python
  vol = np.interp(length, [50, 300], [minvol, maxvol])
  volume.SetMasterVolumeLevel(vol, None)
  ```

### `HAND_TRACKING_MODULE.py`

This module provides a reusable class for detecting and tracking hand movements.

- **Hand Detection:**

```python
def findHands(self, frame, draw=True):
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    self.results = self.hands.process(imgRGB)
    return frame
```

- **Landmark Position Finding:**

```python
def findPosition(self, frame, handNo=0, draw=True):
    lmList = []
    if self.results.multi_hand_landmarks:
        myHand = self.results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList
```

---

## Customization

You can adjust parameters to improve accuracy and responsiveness:

- **Volume Range Mapping:**

```python
# Change these values to adjust sensitivity
vol = np.interp(length, [50, 300], [minvol, maxvol])
```

- `[300]` represents the hand distance range.
- Adjusting these values changes sensitivity.

- **Camera Resolution:**

```python
width, height = 1000, 1000
cap.set(3, width)
cap.set(4, height)
```

Modify to match your webcam capabilities.

- **Hand Detection Sensitivity:**

```python
detector = htm.handDetector()  # Default values
# Change to: detector = htm.handDetector(detectionCon=0.7) for higher confidence
```

---

## Troubleshooting

| Issue | Solution |
|------------------------|-----------------------------------------------|
| Poor detection | Ensure good lighting and a clear background |
| Volume not changing | Check if pycaw is properly installed |
| Erratic volume changes | Adjust the distance range in the interp function |
| No detection | Check webcam functionality |
| Performance issues | Lower camera resolution or FPS |

---

## License

This project is licensed under the MIT License.

---

_Last updated: March 17, 2025_
