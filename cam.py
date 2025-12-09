import cv2
import numpy as np
import subprocess
import time
from ppadb.client import Client as AdbClient

# Connect to ADB
adb = AdbClient(host="127.0.0.1", port=5037)
devices = adb.devices()

if len(devices) == 0:
    print("No device found. Make sure USB Debugging is enabled and ADB is running.")
    exit()

device = devices[0]
print(f"Connected to {device.serial}")

# Start streaming from the phone camera using ADB
device.shell("am start -a android.media.action.VIDEO_CAMERA")
time.sleep(2)  # Give the camera time to open

# Start ADB screen capture loop
while True:
    screenshot = device.screencap()
    
    # Convert the screenshot to an image
    img_np = np.frombuffer(screenshot, dtype=np.uint8)
    frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    if frame is not None:
        frame = cv2.resize(frame, (1280, 720))  # Resize to 720p
        cv2.imshow("Poco X6 Pro Webcam", frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
