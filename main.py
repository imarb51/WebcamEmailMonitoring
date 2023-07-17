import glob
import os
import time
import cv2
from emailing import send_email

video = cv2.VideoCapture(0)
time.sleep(2)
first_frame = None
status_list = []
count = 1

def clean_images():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
while True:
    status = 0
    check,frame = video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame = gray_frame

    delta_frame = cv2.absdiff(first_frame,gray_frame)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame,None,iterations=2)
    cv2.imshow("My Video", dil_frame)
    contours,check = cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_rectangles = glob.glob("images/*.png")
            index = int(len(all_rectangles)/2)
            final_image = all_rectangles[index]


    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email(final_image)
        clean_images()

    print(status_list)
    cv2.imshow("Video",frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()

