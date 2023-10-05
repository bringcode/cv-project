# YOLOv5 🚀 by Ultralytics, AGPL-3.0 license
# python3 yolov5/detect.py --weights ./yolov5/runs/train/direction_detect_yolov5/weights/pre_best.pt --img 416 --conf 0.5 --source 'imgs/arrow.png'

"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources:
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/LNwODJXcvt4'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
"""

import argparse
import csv
import os
import platform
import sys
from pathlib import Path
import torch

# 현재 디렉토리를 Path객체로 FILE 변수에 저장
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from ultralytics.utils.plotting import Annotator, colors, save_one_box

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.torch_utils import select_device, smart_inference_mode


@smart_inference_mode()
class mkyolo():
    def __init__(self):
        pass
    def run(
            self,

            # 예측할 이미지 ========================
            img,
            # weights에 모델의 가중치 경로 설정 =========================
            weights= '/home/pi/robot/Sensor/yolo_model/runs/train/direction_detect_yolov5/weights/best.pt',  # model path or triton URL,

            # source에 예측할 이미지 경로 =============================
            source= '/home/pi/robot/Sensor/yolo_model/imgs/arrow_model.jpeg',  # file/dir/URL/glob/screen/0(webcam)
            data=ROOT / 'data/coco128.yaml',  # dataset.yaml path

            # 예측할 이미지를 어떤 크기로 변형할 것인지 ==========================
            imgsz=(416, 416),  # inference size (height, width)

            # 몇 이상의 정확도를 가졌을 때, 사용할 것인지
            conf_thres=0.25,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            max_det=1000,  # maximum detections per image
            device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            view_img=False,  # show results
            save_txt=False,  # save results to *.txt
            save_csv=False,  # save results in CSV format
            save_conf=False,  # save confidences in --save-txt labels
            save_crop=False,  # save cropped prediction boxes
            nosave=False,  # do not save images/videos
            classes=None,  # filter by class: --class 0, or --class 0 2 3
            agnostic_nms=False,  # class-agnostic NMS
            augment=False,  # augmented inference
            visualize=False,  # visualize features
            update=False,  # update all models
            project=ROOT / 'runs/detect',  # save results to project/name
            name='exp',  # save results to project/name
            exist_ok=False,  # existing project/name ok, do not increment
            line_thickness=3,  # bounding box thickness (pixels)
            hide_labels=False,  # hide labels
            hide_conf=False,  # hide confidences
            half=False,  # use FP16 half-precision inference
            dnn=False,  # use OpenCV DNN for ONNX inference
            vid_stride=1,  # video frame-rate stride
    ):
        source = str(source)
        save_img = not nosave and not source.endswith('.txt')  # save inference images
        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)
        screenshot = source.lower().startswith('screen')
        if is_url and is_file:
            source = check_file(source)  # download

        # Directories
        # save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
        # save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
        # (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Load model
        device = select_device(device)
        model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
        stride, names, pt = model.stride, model.names, model.pt
        imgsz = check_img_size(imgsz, s=stride)  # check image size

        # Dataloader
        bs = 1  # batch_size
        if webcam:
            view_img = check_imshow(warn=True)
            dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
            bs = len(dataset)
        elif screenshot:
            dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
        else:
            # 이 부분이 예측할 데이터를 전처리하는 코드 =====================================
            dataset = LoadImages(source, img, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        vid_path, vid_writer = [None] * bs, [None] * bs

        # Run inference
        model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(model.device)
                im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim

            # Inference
            with dt[1]:
                # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
                pred = model(im, augment=augment, visualize=visualize)

            # NMS
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

            # Second-stage classifier (optional)
            # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

            # Define the path for the CSV file
            # csv_path = save_dir / 'predictions.csv'

            # Create or append to the CSV file
            def write_to_csv(image_name, prediction, confidence):
                data = {'Image Name': image_name, 'Prediction': prediction, 'Confidence': confidence}
                with open(csv_path, mode='a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data.keys())
                    if not csv_path.is_file():
                        writer.writeheader()
                    writer.writerow(data)

            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                if webcam:  # batch_size >= 1
                    p, im0, frame = path[i], im0s[i].copy(), dataset.count
                    s += f'{i}: '
                else:
                    p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

                # p = Path(p)  # to Path
                # save_path = str(save_dir / p.name)  # im.jpg
                # txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
                # s += '%gx%g ' % im.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, 5].unique():
                        n = (det[:, 5] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    # label을 담는 리스트 정의 ============================================
                    labels = []
                    centers = []
                    xyxy_list = []
                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)  # integer class
                        label = names[c] if hide_conf else f'{names[c]}'
                        confidence = float(conf)
                        confidence_str = f'{confidence:.2f}'

                        if save_csv:
                            write_to_csv(p.name, label, confidence_str)

                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                            with open(f'{txt_path}.txt', 'a') as f:
                                f.write(('%g ' * len(line)).rstrip() % line + '\n')

                        if save_img or save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class

                            # label: 화살표 방향을 포함한 label 저장 =========================================================
                            # labels: 복수 개의 label을 담고 있음 =================================
                            labels.append(label)
                            label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                            annotator.box_label(xyxy, label, color=colors(c, True))

                            # Stream results
                            # im0 변수에 annotate된 이미지 저장 ========================================
                            # xyxy 변수에 순차적으로 왼쪽 위 꼭짓점의 x,y값 / 오른쪽 아래 꼭짓점의 x,y값이 저장 ========================================
                            # width: anotation의 폭, height: anotation의 높이, center: 중심좌표, label: 화살표 방향 및 label ========================================

                            im0 = annotator.result()
                            xyxy = list(map(int, xyxy))
                            width = xyxy[2] - xyxy[0]
                            height = xyxy[3] - xyxy[1]
                            center = ((width//2) + xyxy[0], (height//2) + xyxy[1])
                            xyxy_list.append(xyxy)
                            centers.append(center)
                            cv2.circle(im0, center, 3, (255,255,0), cv2.FILLED, cv2.LINE_AA)

                    # centers와 labels, xyxy_list가 매칭되어 저장되어있음
                    # print(labels)
                    # print(centers)
                    # print(xyxy_list)

                    # 골이 들어가있는지를 나타내는 변수 
                    is_goal = False

                    # flag 박스 내에 ball 박스가 완전히 포함되어 있으면 is_goal 변수는 True, 아니면 False
                    if 'flag' in labels and 'ball' in labels:
                        flag_ind = labels.index('flag')
                        ball_ind = labels.index('ball')

                        flag_xyxy = xyxy_list[flag_ind]
                        ball_xyxy = xyxy_list[ball_ind]

                        if ball_xyxy[0] > flag_xyxy[0] and ball_xyxy[2] < flag_xyxy[2] and ball_xyxy[1] > flag_xyxy[1] and ball_xyxy[3] < flag_xyxy[3]:
                            is_goal = True

        im0 = cv2.putText(im0, 'is_goal: {}'.format(is_goal), (10,40), cv2.FONT_HERSHEY_SIMPLEX , 1.5, (0,0,0), 2, cv2.LINE_AA)

        # 결과 이미지 출력
        cv2.imshow('dst', im0)
        cv2.waitKey()

model = mkyolo()

img = cv2.imread('/home/pi/robot/Sensor/yolo_model/imgs/arrow_model.jpeg')
model.run(img)

# ===============================================================================

# 모델 객체 생성
# model = mkyolo()

# 예측하고 싶은 이미지 변수 넣기
# img = cv2.imread('/Users/woojin/Desktop/project/robot-project/imgs/test_3.png')

# import cv2
# cap = cv2.VideoCapture(0) # 해당 경로의 동영상 파일을 가져옴

# while cap.isOpened(): # 동영상 파일이 올바르게 열였는지?
#     ret, frame = cap.read() # ret : 성공여부, frame: 받아온 동영상 이미지(프레임)
#     if not ret: # cap.read()를 통해 동영상을 읽는데 성공했는지?
#         print('더 이상 가져올 프레임이 없어요')
#         break
            
#     prediction = model.run(frame)
#     cv2.imshow('video', prediction) # 받아온 동영상 프레임을 보여줌

#     if cv2.waitKey(25) == ord('q'): # 25ms동안 기다리며 q버튼이 입력됐는지 확인(시간이 짧을수록 동영상 재생속도도 빨라짐)
#         print('사용자의 입력에 의해 종료합니다.')
#         break

# cap.release() # 받아온 자원해제
# cv2.destroyAllWindows() # 모든 창 닫기