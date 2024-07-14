import cv2
import numpy as np
import pyautogui

def update_canny(val):
    threshold1 = cv2.getTrackbarPos('Threshold1', 'Canny Edge Detection')
    threshold2 = cv2.getTrackbarPos('Threshold2', 'Canny Edge Detection')
    print(threshold1, threshold2)
    _, binary_frame = cv2.threshold(gray_frame, threshold1, threshold2, cv2.THRESH_BINARY_INV)
    cv2.imshow('Canny Edge Detection', binary_frame)

screenshot = pyautogui.screenshot()
image = np.array(screenshot)
gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('Canny Edge Detection')

cv2.createTrackbar('Threshold1', 'Canny Edge Detection', 0, 255, update_canny)
cv2.createTrackbar('Threshold2', 'Canny Edge Detection', 0, 255, update_canny)

cv2.setTrackbarPos('Threshold1', 'Canny Edge Detection', 50)
cv2.setTrackbarPos('Threshold2', 'Canny Edge Detection', 150)

update_canny(0)

while True:
    update_canny(0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
