import cv2
import numpy as np

def find_arrow_direction(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary threshold
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the largest contour is the arrow
    c = max(contours, key=cv2.contourArea)

    # Compute the center of the contour using moments
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # Find the point in the contour that is furthest from the center
    max_distance = 0
    # endpoint = None
    endpoint = find_arrow_tip(c, cX, cY)
    for point in c:
        point = point[0]
        distance = np.sqrt((cX - point[0]) ** 2 + (cY - point[1]) ** 2)
        if distance > max_distance:
            max_distance = distance
            endpoint = point

    # Draw the center and the endpoint on the image
    cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
    cv2.circle(image, (endpoint[0], endpoint[1]), 5, (0, 255, 0), -1)
    cv2.line(image, (cX, cY), (endpoint[0], endpoint[1]), (255, 0, 0), 2)

    return image
  
def find_arrow_tip(c, cX, cY):
    largest_angle = 0
    arrow_tip = None

    for i in range(len(c)):
        # Get two adjacent points
        p1 = c[i][0]
        p2 = c[(i + 1) % len(c)][0]
        
        # Compute vectors from the center of the contour to the points
        v1 = [p1[0] - cX, p1[1] - cY]
        v2 = [p2[0] - cX, p2[1] - cY]
        
        # Compute dot product and magnitude of vectors
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        mag1 = np.sqrt(v1[0] ** 2 + v1[1] ** 2)
        mag2 = np.sqrt(v2[0] ** 2 + v2[1] ** 2)
        
        # Compute the angle between vectors using arccosine
        if mag1 * mag2 == 0:  # avoid division by zero
            continue
        angle = np.arccos(dot / (mag1 * mag2))
        
        # Update the arrow tip if this angle is larger than previous
        if angle > largest_angle:
            largest_angle = angle
            arrow_tip = p1

    return arrow_tip


# Read the image containing the arrow
image = cv2.imread('arrow.png')
result = find_arrow_direction(image)

cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()