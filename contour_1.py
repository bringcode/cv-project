import cv2
import numpy as np

cap = cv2.VideoCapture("detection_7.mp4")

scale_percent = 65

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    hsv = cv2.cvtColor(cv2.GaussianBlur(resized_frame, (3, 3), 1), cv2.COLOR_BGR2HSV)

    # Ball Detection
    mask_ball = cv2.inRange(hsv, np.array([0, 150, 120]), np.array([10, 255, 255]))
    mask_ball += cv2.inRange(hsv, np.array([170, 150, 120]), np.array([180, 255, 255]))

    contours_ball, _ = cv2.findContours(mask_ball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_ball) > 0:
        c = max(contours_ball, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 5:
            cv2.circle(resized_frame, (int(x), int(y)), int(radius), (0, 0, 255), 5)

    # Inline and Outline Detection
    inline_mask = cv2.inRange(hsv, np.array([68, 84, 50]), np.array([90, 255, 255]))
    yellow_mask = cv2.inRange(hsv, np.array([20, 50, 100]), np.array([50, 255, 255]))
    inline_mask += yellow_mask
    outline_mask = cv2.inRange(hsv, np.array([80, 65, 0]), np.array([110, 255, 255]))
    
    contours_inline, _ = cv2.findContours(inline_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_outline, _ = cv2.findContours(outline_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours_inline:
        if cv2.contourArea(c) > 100:
            cv2.drawContours(resized_frame, [c], -1, (0, 255, 0), 2)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.putText(resized_frame, "inline", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    for c in contours_outline:
        if cv2.contourArea(c) > 100:
            cv2.drawContours(resized_frame, [c], -1, (255, 0, 0), 2)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.putText(resized_frame, "outline", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow("ResizedFrame", resized_frame)

    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()
