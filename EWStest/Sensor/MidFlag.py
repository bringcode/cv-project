import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        self.farthest_flag_box = None

    def process_frame(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define green and yellow color ranges
        green_mask = cv2.inRange(hsv_frame, (57, 95, 61), (89, 255, 255))
        yellow_mask = cv2.inRange(hsv_frame, (0, 57, 187), (45, 234, 255))

        green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        shape_info_list = []

        for green_contour in green_contours:
            x, y, w, h = cv2.boundingRect(green_contour)
            # Make sure that the yellow_roi does not go out of bounds
            y_start = max(0, y)
            y_end = min(y + h, yellow_mask.shape[0])
            x_start = max(0, x)
            x_end = min(x + w, yellow_mask.shape[1])
            
            yellow_roi = yellow_mask[y_start:y_end, x_start:x_end]

            _, labels, stats, _ = cv2.connectedComponentsWithStats(yellow_roi, connectivity=8)

            for i in range(1, len(stats)):
                x_blob, y_blob, w_blob, h_blob, area_blob = stats[i]

                if area_blob <= 100:
                    continue

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

        flag_boxes = [box for box in shape_info_list if box[1] == "FLAG"]
        if len(flag_boxes) >= 2:
            camera_center = (frame.shape[1] // 2, frame.shape[0])

            max_distance = 0
            farthest_flag_box = None

            for box in flag_boxes:
                box_center = box[0]
                distance = ((box_center[0] - camera_center[0]) ** 2 + (box_center[1] - camera_center[1]) ** 2) ** 0.5

                if distance > max_distance:
                    max_distance = distance
                    farthest_flag_box = box

            for i, box in enumerate(shape_info_list):
                if box[1] == "FLAG" and box != farthest_flag_box:
                    shape_info_list[i] = (box[0], "ARROW")

        for shape_info in shape_info_list:
            center, shape_text = shape_info[0], shape_info[1]
            offset = -10 if shape_text == "FLAG" else 10

            cv2.putText(frame, f'Shape: {shape_text}', (center[0], center[1] + offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = self.process_frame(frame)

            cv2.imshow('Green and Yellow Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 0
    shape_recognition = ShapeRecognition(video_path)
    shape_recognition.run()
