import cv2 as cv
import numpy as np
from roboflow import Roboflow
rf = Roboflow(api_key="7sg8pwBao1WlyoAmuk3W")
project = rf.workspace().project("direction_detect")
model = project.version(1).model

# infer on a local image
img = cv.imread('imgs/arrow.png', cv.IMREAD_COLOR)
prediction = model.predict("imgs/arrow.png", confidence=5, overlap=30).json()

x = int(prediction['predictions'][0]['x'])
y = int(prediction['predictions'][0]['y'])
max_x = int(prediction['image']['width'])
max_y = int(prediction['image']['height'])
direction = prediction['predictions'][0]['class']

# max_x가 max_y보다 크다고 가정
if direction == 'up':
    line_end_x = x
    line_end_y = 0
elif direction == 'left-up':
    if x >= y:
        line_end_x = x - y
        line_end_y = 0
    else:
        line_end_y = y - x
        line_end_x = 0
elif direction == 'right-up':
    if y >= (max_x-x):
        line_end_x = max_x
        line_end_y = y-(max_x-x)
    else:
        line_end_x = x + y
        line_end_y = 0
elif direction == 'left':
    line_end_x = 0
    line_end_y = y
elif direction == 'right':
    line_end_x = max_x
    line_end_y = y
elif direction == 'down':
    line_end_x = x
    line_end_y = max_y
elif direction == 'left-down':
    if x >= (max_y-y):
        line_end_x = x-(max_y-y)
        line_end_y = max_y
    else:
        line_end_x = 0
        line_end_y = x+y
elif direction == 'right-down':
    if (max_x-x) >= (max_y-y):
        y = max_y
        x = x+(max_y-y)
    else:
        x = max_x
        y = y + (max_x-x)


COLOR = (0, 255, 255) # BGR : Yellow 색깔
THICKNESS = 3 # 두께

#선을 넣을 그림, 시작점, 끝점, 색깔, 두께, 선 종류
cv.line(img, (x, y), (line_end_x, line_end_y), COLOR, THICKNESS, cv.LINE_AA)

cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()

# visualize your prediction
# model.predict("imgs/arrow.png", confidence=5, overlap=30).save("prediction.jpg")