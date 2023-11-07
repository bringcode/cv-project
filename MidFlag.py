import numpy as np
import cv2

class ShapeInfo:
    def __init__(self, center, shape):
        self.center = center
        self.shape = shape

class MidFlag:
    def __init__(self, video_path, area_threshold=300):
        self.video_path = video_path
        self.area_threshold = area_threshold
        self.farthest_flag_center = None

    def process(self):
        cap = cv2.VideoCapture(self.video_path, cv2.CAP_V4L)

        if not cap.isOpened():
            print("Error: Could not open video.")
            return None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Green color range
            low_green = np.array([57, 95, 61])
            high_green = np.array([89, 255, 255])
            green_mask = cv2.inRange(hsv_frame, low_green, high_green)
            result_frame = cv2.bitwise_and(frame, frame, mask=green_mask)

            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            green_boxes = [cv2.boundingRect(contour) for contour in contours if cv2.contourArea(contour) > self.area_threshold]

            # Yellow color range
            low_yellow = np.array([22, 93, 0])
            high_yellow = np.array([45, 255, 255])

            shape_info_list = []

            for (x, y, w, h) in green_boxes:
                # Check for yellow within the green
                yellow_mask = cv2.inRange(hsv_frame[y:y+h, x:x+w], low_yellow, high_yellow)
                _, labels, stats, _ = cv2.connectedComponentsWithStats(yellow_mask, connectivity=8)

                for i in range(1, len(stats)):
                    x_blob, y_blob, w_blob, h_blob, area_blob = stats[i]
                    if area_blob >= self.area_threshold:
                        cv2.rectangle(frame, (x + x_blob, y + y_blob), (x + x_blob + w_blob, y + y_blob + h_blob), (0, 255, 0), 2)

                        # Calculate the center of the yellow region
                        center_x = x + x_blob + w_blob // 2
                        center_y = y + y_blob + h_blob // 2
                        center = (center_x, center_y)

                        # Shape classification logic can be added here, for simplicity assuming all are flags
                        shape_info = ShapeInfo(center, "FLAG")
                        shape_info_list.append(shape_info)

            # Custom condition logic (e.g., filter, sort shapes)
            flag_boxes = [box for box in shape_info_list if box.shape == "FLAG"]
            if len(flag_boxes) >= 2:
                flag_boxes.sort(key=lambda box: cv2.norm(box.center, (frame.shape[1] // 2, frame.shape[0])))
                self.farthest_flag_center = flag_boxes[-1].center
                for box in flag_boxes[:-1]:
                    box.shape = "ARROW"

            for shape_info in shape_info_list:
                center, shape_text = shape_info.center, shape_info.shape
                cv2.putText(frame, f'Shape: {shape_text}', (center[0], center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return self.farthest_flag_center

if __name__ == "__main__":
    # Camera source or video file path
    processor = MidFlag(0, 300)  # If using a video file, replace 0 with the file path
    farthest_flag_center = processor.process()
    print(f"Farthest FLAG Center: {farthest_flag_center}")
