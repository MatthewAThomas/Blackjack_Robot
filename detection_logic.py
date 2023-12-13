import cv2
import numpy as np
import pytesseract
import time

NUM_SHOTS = 10 #number of images that we get

""" Returns a video capture object """


fail = False

def init_detection():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error opening video")
        exit(-1)

    ret, frame = cap.read()
    height, width, _ = frame.shape
    cv2.namedWindow('Raw Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Raw Image', width, height)

    return cap


""" Returns the card number. Returns [] if unsuccesful """
def detect_card(cap):

    card_images = []
    count = 0
    fail_count = 0

    # for _ in range(NUM_SHOTS):
    while count < 7 and fail_count < 10:
        ret, frame = cap.read()

        if not ret:
            break

        # Format the raw image
        flipped_frame = cv2.flip(frame, -1)

        x,y,h,w = 0,50,240,320
        # frame = flipped_frame[180:350, 240:340] #height and width
        frame = flipped_frame[180:340, 250:360] #height and width
    
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.GaussianBlur(frame, (5,5), 0)

        # _, frame = cv2.threshold(frame, 30, 200, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, frame = cv2.threshold(frame, 30, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Show the formatted image
        cv2.imshow('Raw Image', frame)

        # Find the card number
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Replace with the actual path from 'which tesseract'
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=2345678910AJQK'
        text = pytesseract.image_to_string(frame, config=custom_config)
        
        # print("type is", type(text))
        # print("length of the string is ", len(text))
        
        #  card_images.append(text)
        if text.strip():
            single_char = text.strip()[0]
            card_images.append(single_char)
            count = count + 1
        else:
            print("Failed to detect")
            print(fail_count)
            # time.sleep(0.5)
            fail_count = fail_count + 1
            # single_char = '*'
            # card_images.append(single_char)

        # DEBUGGING 
        # print(f"card detected: {text}")

        # Check for the 'q' key to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return '*'

    if fail_count >= 10:
        card = input("Enter card: ")
        card = card.upper()
        card = card[0]
        return card
        
    # Return the 
    ret_val = max(card_images,key=card_images.count)
    if len(ret_val) > 1:
        print('There was a tie in reading card')
        print(ret_val)
        ret_val = ret_val[0]

    # print('sanity check inside detection logic')
    print("camera read ", ret_val)
    # if ret_val.strip():
    #     # try:
    #     #     single_char = text.strip()[0]
    #     #     print("Detected:", single_char)
    #     # except Exception:
    #     #     print("something wrong")
    #     return ""

    # else:
    #     print("No text detected")

    # print("inside the detectio function")
    # print(type(ret_val))
    # # DEBUGGING 
    # print(f"ret_val: {ret_val[0], ret_val[1], ret_val[2]}")
    # print("reading",  ret_val)

    return ret_val


def close_detection(cap):
    # Release the capture object and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()


#ret, frame = cap.read()
    # if ret:
    #     height, width, _ = frame.shape
    #     cv2.namedWindow('Raw Image', cv2.WINDOW_NORMAL)
    #     cv2.resizeWindow('Raw Image', width, height)
    #     print("width ", width)
    #     print("height ", height)
