from .StepCounter import StepCounter
from .Detectors import FaceDetector
from ultralytics import YOLO
from datetime import datetime
from .utils import Visualizer
import numpy as np
import cv2 as cv
import time as time

class Tracker:
    """
    Tracking perons and generate Path canvas for each person.
    Arguments:
        unique_ids: set = set of unique ids.
        person_canvas: dict = Dictionary of person canvas, it has 
        * 'canvas': person path
        * 'enter_time': time of entering the frame
        * 'enter_point': point of entering the frame
    """
    def __init__(self, video_fbs) -> None:
        self.unique_ids = set()
        self.person_canvas = {}
        self.__video_fbs = video_fbs
        self.__pTime = 0
        self.step_counter = StepCounter()
        self.face_detector = FaceDetector()
        
        # self.plates_detection_model = YOLO("models\license_plate_detector.pt")
        
    def __len__(self) -> int:
        """
        Returns: Number of unique persons tracked.
        """
        return len(self.unique_ids)
    
    def start_tracking(self, frame, tracks, fps = None, draw_canvas:bool = False, distace_using_speed:bool = False, distance_using_steps:bool = False,draw_distance_line:bool = True, detect_faces:bool = False) -> any:
        """
        Start The tracking process. drawing boxes, showing some data and extract paths. also you can calculate distances.
        Parameters:
            frame = The frame of the video to modify it and show the data.
            tracks = The tracks of the person.
            draw_canvas: bool (default = False)= if you want to draw canvas paths.
            draw_distance_line: bool (default = False)= Calculate the distance and show distance lines.
            fpss: list = list of frame per second [Video FBS, Tracker FBS], to make the distance invarient to FBS rates.
        """
        boxes = tracks.boxes
        classes = tracks.names
        keypoints = tracks.keypoints
        
        if (tracks.boxes.is_track): # Is Tracking?
            for person_box in boxes:
                person_class = classes[person_box.cls.item()]
                person_id = person_box.id.item()
                
                cx, cy, w, h = person_box.xywh[0]
                x1, y1, x2, y2 = person_box.xyxy[0]
                
                if (person_class == 'car'):
                    car_frame = frame[int(y1) :int(y2), int(x1):int(x2)]
                    car_plate = self.plates_detection_model(car_frame)
                    if car_plate[0].boxes.cls.numel() > 0:
                        Visualizer.draw_detection_box(frame, car_plate[0].boxes.xyxy[0], "Car Plate")
                        p_x1, p_y1, p_x2, p_y2 = car_plate[0].boxes.xyxy[0]
                        plate_frame = car_frame[int(p_y1):int(p_y2), int(p_x1):int(p_x2)]
                        self.plate_detector.detect(plate_frame)
                
                Visualizer.draw_detection_box(frame, person_box.xyxy[0], "ID:" + str(int(person_id))+ " " + str(person_class))
                
                
                person_box_frame = frame[int(y1) :int(y2), int(x1):int(x2)]
                if (person_id not in self.unique_ids) & (person_id not in self.person_canvas.keys()):
                    detected_face = self.face_detector.detect(person_box_frame,previous_face_width = 0, person_id = person_id)
                    self.unique_ids.add(person_id)
                    self.person_canvas[person_id] = {'canvas':np.zeros((frame.shape[0] , frame.shape[1] , 3), np.uint8),
                                                     'enter_time': datetime.now().ctime(),
                                                     'enter_point': (int(cx) , int(cy) + int(h/2)),
                                                     'exit_time':None,
                                                     'exit_point':None,
                                                     'line_lenght':None,
                                                     'steps_lenght': None,
                                                      # TODO you may face problems here when value = null
                                                     'face': detected_face if(detected_face is not None) else np.zeros((0 , 0, 3), np.uint8) 
                                                     }
                    # img = img[ int(bboxC.ymin * h):int(bboxC.ymin * h)+int(bboxC.height * h) ,int(bboxC.xmin * w):int(bboxC.xmin * w)+ int(bboxC.width * w)]
                else:
                    # Update the person exit time
                    self.person_canvas[person_id]['exit_time'] = datetime.now().ctime()
                    self.person_canvas[person_id]['exit_point'] = (int(cx) , int(cy) + int(h/2))
                
                    # Start Calcualte the distance
                    # Using Normal Speed Average
                    if (distace_using_speed):
                        assert fps != None , "Please provide the fps of the video"
                        self.__calculate_distance_speed(frame, person_id, draw_distance_line, [self.__video_fbs, fps])
                    # Using Step Count
                    if (distance_using_steps): frame = self.__calculate_distance_steps(frame, keypoints.xy, boxes.id, person_id, draw_distance_line = draw_distance_line and not distace_using_speed)
                    
                cv.putText(frame , str(len(self.unique_ids)) + " People "+ str(len(boxes)) + " Now" , (10,30) , cv.FONT_HERSHEY_SIMPLEX , 1 , (0,255,0) , 3)
                
                if (detect_faces):
                    detected_face = self.face_detector.detect(person_box_frame,previous_face_width = self.person_canvas[person_id]['face'].shape[1], person_id = person_id)
                    self.person_canvas[person_id]['face'] = detected_face if (detected_face is not None) else self.person_canvas[person_id]['face']
                frame = self.__draw_person_canvas(frame,person_id, person_box.xyxy[0], draw_canvas)

        return frame
    
    
    def __calculate_distance_speed(self, frame, person_id:int, draw_distance_line:bool, fpss: list, avg_speed:float = 3.1) -> any:
        """
        Distance calculator depending on time, and average person speed in normal times
        NOTE that this is so sensitive to the local time, and video lagging. 
        Tried to solve that as well as possible.
        Parameters:
            frame = The frame of the video to modify it and show the data.
            person_id = The id of the person.
            draw_distance_line: bool = To draw the distance line.
            fpss: list = list of frame per second [Video FBS, Tracker FBS], to make the distance invarient to FBS rates.
            avg_speed: float (default = 3.1 mile/hour)= Average person speed in normal times.
        """
        enter_time = self.person_canvas[person_id]['enter_time']
        exit_time = self.person_canvas[person_id]['exit_time']
        enter_timestamp = datetime.strptime(enter_time, '%a %b %d %H:%M:%S %Y')
        exit_timestamp = datetime.strptime(exit_time, '%a %b %d %H:%M:%S %Y')
        
        existence_time = (exit_timestamp - enter_timestamp).total_seconds() / 60  # per minute to avoid very small numbers.
        mileshour_to_meterminutes = 26.8224 * avg_speed
                
        if fpss[0] > fpss[1]:
            # Delay
            delay_ratio = (fpss[0] - fpss[1]) / fpss[0]
        elif fpss[0] < fpss[1]:
            # Fast
            delay_ratio = (fpss[0] - fpss[1]) / fpss[0]
        else:
            delay_ratio = 0
        
        
        # space = existence_time * mileshour_to_meterminutes * (abs(fpss[1]-fpss[0]) / fpss[0])
        space = existence_time * mileshour_to_meterminutes - (delay_ratio * existence_time * mileshour_to_meterminutes)
        
        
        print("----")
        print("Space "+str(space))
        print("Enter "+str(enter_timestamp)+ " Leave "+ str(exit_timestamp)+ " --> " + str(existence_time))
        print("FBS Sub "+ str(abs(fpss[1]-fpss[0]) / fpss[0]))
        print("Vid FBS " + str(fpss[0]) + " Real FBS " + str(fpss[1]))
        print("----")
        
        
        self.person_canvas[person_id]['line_lenght'] = space
        
        if draw_distance_line:
            Visualizer.draw_line(frame, self.person_canvas[person_id]['enter_point'], self.person_canvas[person_id]['exit_point'], str(int(space)) + " Meters")

    
    def __calculate_distance_steps(self, frame, keypoints, ids, tracked_id:int, draw_distance_line:bool = False):
        frame, steps, distance =  self.step_counter.steps_counter(frame = frame,keypoints = keypoints, ids = ids, tracked_person_id = tracked_id)
        self.person_canvas[tracked_id]['steps_lenght'] = [steps, distance]
        
        if draw_distance_line:
            Visualizer.draw_line(frame, self.person_canvas[tracked_id]['enter_point'], self.person_canvas[tracked_id]['exit_point'], str(int(distance)) + " Meters")
        
        return frame
    
        
    def currentFBS(self) -> int:
        """
        Counting the realtime FBS. to make the distance invarient to FBS rates ups and downs.
        Parameters:
        Return:
            current_fbs:int  = The realtime FBS.
        """
        cTime = time.time()
        current_fbs = 1/(cTime - self.__pTime)
        self.__pTime = cTime
        return int(current_fbs)
    
    
    def __draw_person_canvas(self, frame, person_id:int, xyxy, show_canvas:bool) -> any:
        """
        Drawing the path of the person in canvas and save it in the dictionary.
        Parameters:
            frame = The frame of the video to modify it and show the steps.
            person_id = The id of the person. to modify his canvas.
            xyxy = The x1,y1,x2,y2 cordinates values of the person_box.
            show_canvas: bool = if you want to show the canvas.
        Return:
            frame = the modified frame
        """
        x1, _, x2, y2 = xyxy
        personal_canvas = self.person_canvas[person_id]['canvas']
        Visualizer.draw_point(personal_canvas, (int(x2) + int((x1 - x2)/2 ) , int(y2)))
        if show_canvas:frame = self.__merge_canvas_frame(frame , personal_canvas)
        self.person_canvas[person_id]['canvas'] = personal_canvas
        return frame
    
    def __merge_canvas_frame(self, frame, canvas) -> any:
        """
        Merging two matrix(frames) together.
        Parameters:
            frame = The frame of the video to modify it and show the steps.
            canvas = The canvas of the person.
        Return:
            frame = bitwise-or of the given frames.
        """
        return cv.bitwise_or(frame , canvas)
