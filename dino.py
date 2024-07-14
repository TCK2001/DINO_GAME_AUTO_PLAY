import cv2
import numpy as np
import pyautogui
from pynput import mouse

"""
Dino game website : https://chromedino.com/
"""

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
        
def capture_screen_region_pyautogui(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img
 
def pre_process(_imgCrop):
    gray_frame = cv2.cvtColor(_imgCrop, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY_INV)
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
 
def game_logic(conFound, _imgContours, jump_distance=35):
    if conFound:
        left_most_contour = min(conFound, key=lambda cnt: cv2.boundingRect(cnt)[0])
        x, y, w, h = cv2.boundingRect(left_most_contour)

        cv2.line(_imgContours, (0, y), (x, y), (0, 200, 0), 10)

        if x < jump_distance:
            pyautogui.press("space")
            print("Jump")
 
    return _imgContours

if __name__ == '__main__':
    mouse_x, mouse_y = 0, 0
    save_coor = []
    
    print("""
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@ DINO GAME @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DINO GAME @@@
            @@@@@@@@@@@@@@@@@@@@@@@@ DINO GAME @@@@@@@@@@@@@@@@@@@@@@@@@
            @@@ DINO GAME @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DINO GAME @@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            """)
    
    while True:
        try :
            if len(save_coor) < 4 :
                print("Now : ", len(save_coor))
                print("Select your Start_xy and End_xy")
                get_mouse_position()
                continue
            
            # Step 1 - Capture the screen region of game
            imgGame = capture_screen_region_pyautogui(save_coor[0], save_coor[1], (save_coor[2] - save_coor[0]), (save_coor[3] - save_coor[1]))
            # cv2.imshow("Game", imgGame)
            
            # Step 2 - Crop the image to the desired region
            cp = 35, 180, 200
            imgCrop = imgGame[cp[0]:cp[1], cp[2]:]
            # cv2.imshow("Crop_Game", imgCrop)
            
            # Step 3 - Pre-Process Image
            imgPre = pre_process(imgCrop)
            # cv2.imshow("pre_img", imgPre)

            # Step 4 - Find Contour
            imgContours, conFound = find_obstacles(imgCrop, imgPre)
            # cv2.imshow("Game2", imgContours)

            # Step 5 - game logic => jumping
            imgContours = game_logic(conFound, imgContours)         
            cv2.imshow("laddar detect", imgContours)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"ERROR: {e}")
            save_coor = []
            print("Please recrop the area.")
            continue

    cv2.destroyAllWindows()