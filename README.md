# DINO_GAME_CV2
## DEMO Video
![dino_res](https://github.com/user-attachments/assets/0822cc19-ee4f-4376-b44a-25d170fadc75)

## Enviroment
Python 3.11.4
cv2
numpy
pyautogui
pynput 

## Dino Website [Link](https://chromedino.com/)
```
https://chromedino.com/
```

### 🔥Step 1🔥
Open the above link [Dino Website](https://chromedino.com/)

### 🔥Step 2🔥
Select the two point ( ex : start_x, start_y, end_x, end_y)
look at the below example picture.
![image](https://github.com/user-attachments/assets/eef4ae92-915f-4f1f-b05e-12cb88a834c6)
```python
# Each coordinate save in mouse_x, mouse_y
def on_click(x, y, button, pressed):
    global mouse_x, mouse_y, save_coor
    if pressed:
        mouse_x, mouse_y = x, y
        save_coor.append(mouse_x)
        save_coor.append(mouse_y)
        return False   

def get_mouse_position():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()     
````

### 🔥Step 3🔥 
Captured a screenshot of the user screen
```python
def capture_screen_region_pyautogui(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img
```

### 🔥Step 4🔥
Pre-Processing the cropped image + find the target object (need avoid object)
You can't do the pre-processing. Just directly find the contours in the cropped image, but there is a lot of noise in it.
Also you have to using **find_the_best_threshold.py** to find the optimize threshold.
```python
def pre_process(_imgCrop):
    gray_frame = cv2.cvtColor(_imgCrop, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY_INV)
    canny_frame = cv2.Canny(binary_frame, 50, 50)
    kernel = np.ones((5, 5))
    dilated_frame = cv2.dilate(canny_frame, kernel, iterations=2)
    
    return dilated_frame
 
 
def find_obstacles(_imgCrop, _imgPre):
    contours, _ = cv2.findContours(_imgPre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imgContours = _imgCrop.copy()
    conFound = []

    for contour in contours:
        if cv2.contourArea(contour) > 350:
            conFound.append(contour)
    
    cv2.drawContours(imgContours, conFound, -1, (0, 255, 0), 2)
    
    return imgContours, conFound
```

### 🔥Step 5🔥
Finally, you need to know the distance at which the dino has to jump.
( A recommended jump distance of 35 to 50 is the best. )
```python
def game_logic(conFound, _imgContours, jump_distance=40):
    if conFound:
        left_most_contour = min(conFound, key=lambda cnt: cv2.boundingRect(cnt)[0])
        x, y, w, h = cv2.boundingRect(left_most_contour)

        cv2.line(_imgContours, (0, y), (x, y), (0, 200, 0), 10)

        if x < jump_distance:
            pyautogui.press("space")
            print("Jump")
 
    return _imgContours
```

Enjoy it !!!!!!!!
