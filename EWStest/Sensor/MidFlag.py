import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        if not self.cap.isOpened():
            raise ValueError(f"Video at {video_path} cannot be opened")
        self.green_boxes = []
        self.flags = []  # List to store recognized flags
        self.arrows = []  # List to store recognized arrows

    def merge_close_boxes(self, boxes, threshold=50):
        # Merge boxes that are close to each other
        merged_boxes = []
        while boxes:
            box = boxes.pop(0)
            x, y, w, h = box
            boxes_to_merge = [box]

            # Check each box to see if it is close to the current box
            for other_box in boxes:
                ox, oy, ow, oh = other_box
                distance = np.sqrt((x + w/2 - (ox + ow/2))**2 + (y + h/2 - (oy + oh/2))**2)
                if distance < threshold:
                    boxes_to_merge.append(other_box)

            # Merge all boxes that are close to the current box
            for box_to_merge in boxes_to_merge:
                if box_to_merge in boxes:
                    boxes.remove(box_to_merge)
                    ox, oy, ow, oh = box_to_merge
                    x = min(x, ox)
                    y = min(y, oy)
                    w = max(x + w, ox + ow) - x
                    h = max(y + h, oy + oh) - y

            # Add the merged box to the list of merged boxes
            merged_boxes.append((x, y, w, h))
        return merged_boxes

    def process_frame(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define green range
        low_green = np.array([57, 78, 61])
        high_green = np.array([71, 140, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        result_frame = cv2.bitwise_and(frame, frame, mask=green_mask)
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        green_boxes = [cv2.boundingRect(contour) for contour in contours]

        # Merge close green boxes
        merged_green_boxes = self.merge_close_boxes(green_boxes)
        self.green_boxes = merged_green_boxes

        # Rest of the code remains the same...

    # Rest of the class remains the same...

if __name__ == "__main__":
    video_path = 0  # Use 0 for webcam
    shape_recognition = ShapeRecognition(video_path)
    shape_recognition.run()
