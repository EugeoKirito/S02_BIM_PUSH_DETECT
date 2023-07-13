# YOLOv5 🚀 by Ultralytics, AGPL-3.0 license
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
                                                     'https://youtu.be/Zgi9g1ksQHc'  # YouTube
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
import os
import platform
import random
import sys
import time
from pathlib import Path
import torch
import PySimpleGUI as sg
import threading
import datetime
import random
from count_up import update_count
li = [0,0,0,0,0,0,0]

# GPIO
try:
    sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
    sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
    import Jetson.GPIO as GPIO
except Exception as e:
    print(e)

led1 = 15
led2 = 16
led3 = 18

# 设置GPIO初始口
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(led1, GPIO.OUT)
# GPIO.setup(led2, GPIO.OUT)
# GPIO.setup(led3, GPIO.OUT)


# 提醒该load_board
def load_board():
    time.sleep(5)
    # GPIO.output(led1, 1)
    # time.sleep(2)
    # GPIO.output(led1, 0)
    # GPIO.output(led2, 0)
    # time.sleep(2)


# 外层先 设置layout与 主题
theme_dict = {'BACKGROUND': '#223C5F',
              'TEXT': '#ADC7B5',
              'INPUT': '#F2EFE8',
              'TEXT_INPUT': '#000000',
              'SCROLL': '#F2EFE8',
              'BUTTON': ('#000000', '#C2D4D8'),
              'PROGRESS': ('#FFFFFF', '#C7D5E0'),
              'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
BORDER_COLOR = '#223C5F'
DARK_HEADER_COLOR = '#223C5F'
BPAD_TOP = ((20, 20), (20, 10))
BPAD_LEFT = ((20, 10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10, 20), (10, 20))

top_banner = [[sg.Text('1E_BIM_PUSH_ACTION_DETECT' + ' ' * 64, font='Any 20', background_color=DARK_HEADER_COLOR),
               ]]



top = [[sg.Text('                Smart Detect Result', size=(50, 50),
                justification='c', pad=BPAD_TOP, font='Any 20')]]


block_2 = [[sg.Text('OK图片', font='Any 20')],
           [sg.Image(filename='', key="-abnormal-image-")],
           ]
block_3 = [[sg.Text('NG图片', font='Any 20')],
           [sg.Image(key='-static-image-')]
           ]
block_4 = [[sg.Text('YoloV5 AI Judge', size=(15, 1), font='Helvetica 20')],
           [sg.Image(filename='', key='-image-')],
           [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]]
layout = [[sg.Column(top_banner, size=(1050, 38), pad=(0, 0), background_color=DARK_HEADER_COLOR)],
          [sg.Column(top, size=(1010, 80), pad=BPAD_TOP)],
          [sg.Column([[sg.Column(block_3, size=(450, 300), pad=BPAD_LEFT_INSIDE)],
                      [sg.Column(block_2, size=(450, 250), pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT,
                     background_color=BORDER_COLOR),
           sg.Column(block_4, size=(540, 570), pad=BPAD_RIGHT)]
          ]

# 此项不可删除
# label_li = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
label_li = [1, 1, 1, 1]
push_count = 1
# alarm_list = [1,1,1,1,1,1,1,1,1,1]#全是free状态
alarm_list = [] #统计全是1的20帧列表
count_f = 0
sent_message = [0 for i in range(50)] #统计alarm为20个1 的时候记录 下来1个1

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode


# 逻辑仲裁
def logistic_arbitration():
    pass


'''
Step1: 找到图片路径                                       
Step2：列表判断  [free  load   push   load]---->normal    这个已完成
Step3: UI design  ----->  Wenlong 
Step4：GPIO Note  
Step5：tornado message send
'''

today = datetime.datetime.now().weekday() + 1
window = sg.Window('Smart Detect Result Dashboard ', layout, margins=(0, 0), background_color=BORDER_COLOR,
                       no_titlebar=True, grab_anywhere=True )
image_elem = window['-image-']  # Vedio Element
pic_elem = window['-abnormal-image-']  # Pic Element
statis_elem = window['-static-image-']

def gui_run():
        while True:
            event, values = window.read(timeout=250)

t1 = threading.Thread(target=gui_run)
t1.start()
@smart_inference_mode()
def run(
        weights=ROOT / 'yolov5s.pt',  # model path or triton URL
        source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
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




    global push_count, label_li, alarm_list, count_f, sent_message,window,li
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)
    screenshot = source.lower().startswith('screen')
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

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
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
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
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
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
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(f'{txt_path}.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))
                    if save_crop:
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

                '''
This is Sheepyey coding.
---------------------------------Start
                '''

                im0 = cv2.transpose(im0)
                now_ = datetime.datetime.now()
                current_time = now_.strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(im0, current_time, (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (255, 255, 250), 3)
                # 向列表中添加label 名字 保持list的总长为4  即normal-----[0,1,2,1]
                try:
                    # 此处得添加try函数 否则会空列表
                    for info_single_li in reversed(det):
                        # NG判断
                        if count_f < 20:
                            alarm_list.append(int(det[0][-1]))
                        if count_f > 20:
                            alarm_list.append(int(det[0][-1]))
                            del alarm_list[0]
                        count_f = count_f + 1
                        print(count_f)
                        if count_f == 5000:
                            count_f = 21
                        # OK判断
                        if label_li[-1] != det[0][-1]:  # 尾巴与读取的不相同才添加
                            label_li.append(int(det[0][-1]))  # 在末尾插入label_name
                            del label_li[0]  # 删除第一个元素
                        print(
                            info_single_li)  # tensor([510.00000, 268.00000, 877.00000, 390.00000, 0.92271,1.00000]) 后两个是我门想要的置信度以及标签序号

                except Exception as e:
                    print(e)  # 打印报错

                print(label_li)
                print(alarm_list)
                print(sent_message)
                # 加字幕  OK判断
                # cv2.putText(im0, str(alarm_list), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 250), 2)
                # 判断列表[0,1,2,1] 是否是 normal 状态
                # 0 push   1 free   2 load

                if label_li == [1, 2, 0, 2]:  # 此处会有一个BUG 假动作会一直触发target
                    label_li = [2, 0, 2, 1]  # reset 列表 进行重置操作
                    # 完成push动作时候 重置alarm_list、sent_message
                    alarm_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    sent_message = [0 for i in range(50)]
                    # del alarm_list[0]
                    # alarm_list.append(1)
                    push_count += 1
                    t = threading.Thread(target=update_count,args=(push_count,today,li))
                    t.start()

                    # 把push动作更新到UI上
                    pic = cv2.resize(im0, (433, 220), interpolation=cv2.INTER_CUBIC)
                    abnormal_pic = cv2.imencode('.png', pic)[1].tobytes()
                    pic_elem.update(data=abnormal_pic)
                    print("Push Over！")

                #可选选项 可以注释掉  因为本身没加载板子
                # if label_li[-1] == 2: #load状态下 也重置  这个是可选选项
                #     alarm_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                #     sent_message = [0 for i in range(50)]

                # NG判断 必须打开盖子
                if alarm_list == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
                    sent_message.append(1)  # 会一直累加 得到push的时候负值为0
                    del sent_message[0]

                # 多线程
                def NG_NOTE(sent_message):
                    if push_count >= 1: # 从第一次压的动作后开始检测
                        if sum(sent_message) == 50:  # 控制多少帧NG  40X20
                            sent_message = [0 for i in range(50)]
                            print("动作超时,请Load背板,并Push")
                            load_board()
                            cv2.putText(im0, current_time, (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                        (255, 255, 250), 3)
                            pic = cv2.resize(im0, (433, 220), interpolation=cv2.INTER_CUBIC)
                            abnormal_pic = cv2.imencode('.png', pic)[1].tobytes()
                            statis_elem.update(data=abnormal_pic)

                t2 = threading.Thread(target=NG_NOTE, args=(sent_message,))
                t2.start()
                '''
------------------------End
                '''
            # Stream results
            im0 = annotator.result()
            im0 = cv2.transpose(im0)
            # im0 = cv2.flip(im0, -1)
            # 更新窗口
            im0 = cv2.resize(im0, (600, 600), interpolation=cv2.INTER_CUBIC)
            imgbytes = cv2.imencode('.png', im0)[1].tobytes()  # ditto
            image_elem.update(data=imgbytes)

            if view_img:
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                # cv2.imshow(str(p), im0)
                # cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer[i].write(im0)

        # Print time (inference-only)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'runs/train/exp/weights/best.pt',
                        help='model path or triton URL')
    # ROOT / 'data/images'
    #
    parser.add_argument('--source', type=str, default= ROOT / 'data/images', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16   inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt


def main(opt):
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))


if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
    print(push_count)
