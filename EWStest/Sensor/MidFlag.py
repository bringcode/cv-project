import numpy as np
import cv2

class ShapeDetection:
    def __init__(self, video_source=0):
        self.cap = cv2.VideoCapture(video_source)
        self.green_boxes = []
        self.farthest_flag_box = None

    def detect_shapes(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            low_green = np.array([57, 95, 61])
            high_green = np.array([89, 255, 255])

            green_mask = cv2.inRange(hsv_frame, low_green, high_green)

            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.green_boxes = [cv2.boundingRect(contour) for contour in contours]

            low_yellow = np.array([0, 57, 187])
            high_yellow = np.array([45, 234, 255])
            yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)

            shape_info_list = []

            for green_box in self.green_boxes:
                x, y, w, h = green_box
                yellow_roi = yellow_mask[y:y + h, x:x + w]

                _, labels, stats, _ = cv2.connectedComponentsWithStats(yellow_roi, connectivity=8)

                for i in range(1, len(stats)):
                    x_blob, y_blob, w_blob, h_blob, area_blob = stats[i]

                    if area_blob <= 100:
                        continue

                    cv2.rectangle(frame, (x + x_blob, y + y_blob), (x + x_blob + w_blob, y + y_blob + h_blob), (0, 255, 0), 2)

                    yellow_binary = np.zeros_like(yellow_roi)
                    yellow_binary[y_blob:y_blob + h_blob, x_blob:x_blob + w_blob] = yellow_roi[y_blob:y_blob + h_blob, x_blob:x_blob + w_blob]

                    yellow_contours, _ = cv2.findContours(yellow_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    for contour in yellow_contours:
                        epsilon = 0.04 * cv2.arcLength(contour, True)
                        approx = cv2.approxPolyDP(contour, epsilon, True)
                        num_vertices = len(approx)

                        shape_text = "ARROW" if 7 <= num_vertices <= 8 else "FLAG"

                        center_x = x + x_blob + w_blob // 2
                        center_y = y + y_blob + h_blob // 2
                        center = (center_x, center_y)

                        shape_info_list.append((center, shape_text))

            custom_condition = True

            if custom_condition:
                flag_boxes = [box for box in shape_info_list if box[1] == "FLAG"]
                if len(flag_boxes) >= 2:
                    camera_center = (frame.shape[1] // 2, frame.shape[0])
                    max_distance = 0

                    for box in flag_boxes:
                        box_center = box[0]
                        distance = ((box_center[0] - camera_center[0]) ** 2 + (box_center[1] - camera_center[1]) ** 2) ** 0.5

                        if distance > max_distance:
                            max_distance = distance
                            self.farthest_flag_box = box

                    for i, box in enumerate(shape_info_list):
                        if box[1] == "FLAG" and box != self.farthest_flag_box:
                            shape_info_list[i] = (box[0], "ARROW")

            if self.farthest_flag_box is not None:
                farthest_center = self.farthest_flag_box[0]
                print("Farthest FLAG Center:", farthest_center)

            for shape_info in shape_info_list:
                center, shape_text = shape_info[0], shape_info[1]
                offset = 10

                if shape_text == "FLAG":
                    cv2.putText(frame, f'Shape: {shape_text}', (center[0], center[1] - offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, f'Shape: {shape_text}', (center[0], center[1] + offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('Green and Yellow Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    shape_detection = ShapeDetection()
    shape_detection.detect_shapes()
