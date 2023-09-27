# -*- coding: utf-8 -*-
import numpy as np
import cv2

# Open the video file (change the filename as needed)
cap = cv2.VideoCapture(0)

# Filter and font-related variables
kernel = np.ones((5, 5), 'uint8')

while True:
    ret, img = cap.read()
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Color range for red
    lower = np.array([28, 180, 109])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)

    # Color range for yellow
    lower_flag = np.array([20, 68, 130])
    upper_flag = np.array([66, 255, 255])
    mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)

    # Morphological operations
    d_img = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=3)
    f_img = cv2.morphologyEx(mask_flag, cv2.MORPH_CLOSE, kernel, iterations=11)

    # Find red regions
    cont, hei = cv2.findContours(d_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key=cv2.contourArea, reverse=True)[:1]

    red_boxes = []

    for cnt in cont:
        if 100 < cv2.contourArea(cnt) < 306000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            red_boxes.append(box)
            cv2.drawContours(img, [box], -1, (0, 0, 255), 3)

    # Find yellow regions
    cont2, hei2 = cv2.findContours(f_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont2 = sorted(cont2, key=cv2.contourArea, reverse=True)[:1]

    yellow_boxes = []

    for cnt in cont2:
        if 100 < cv2.contourArea(cnt) < 306000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            yellow_boxes.append(box)
            cv2.drawContours(img, [box], -1, (0, 255, 255), 3)

    # Check if red boxes are inside yellow boxes
    for red_box in red_boxes:
        is_inside = False
        for yellow_box in yellow_boxes:
            for point in red_box:
                x, y = point
                if yellow_box[0][0] <= x <= yellow_box[1][0] and yellow_box[0][1] <= y <= yellow_box[2][1]:
                    is_inside = True
                    break
            if is_inside:
                print('goal')
                cv2.drawContours(img, [red_box], -1, (0, 0, 255), 3)
                break
        if not is_inside:
            print('no goal')

    resized_img_1 = cv2.resize(img, dsize=(800, 500), interpolation=cv2.INTER_LINEAR)
    cv2.imshow('Object Dist Measure ', resized_img_1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()