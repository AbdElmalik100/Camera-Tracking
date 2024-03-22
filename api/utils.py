import cv2 as cv
from enum import Enum

class Colors(Enum):
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
class ShapeColors(Enum):
    Points = Colors.BLUE.value

class Visualizer:
    
    @staticmethod
    def draw_bounding_box(xyxy, color = Colors.RED.value):
        """
        Drawing a bounding box Surrounding the full Detected Item.
        Parameters:
        Return:
        """ 
        x1, y1, x2, y2 = xyxy
        pass
    
    @staticmethod
    def draw_detection_box(frame, xyxy, text_data, color = Colors.GREEN.value):
        """
        Drawing Detection Boxs
        NOTE: it draws a bounding box inplace, without a return
        Parameters:
        Return:
        """ 
        x1, y1, x2, y2 = xyxy
        ## Showing person Data
        cv.putText(frame,text_data, (int(x1) , int(y1) - 10), 2, 0.7, color)
        ## Drawing Detection Box (ID , Class)
        cv.rectangle(frame, (int(x1) , int(y1)) , (int(x2) , int(y2)) , (255,0,0) , 3)
    
    @staticmethod
    def draw_point(frame, location_point, color = Colors.GREEN.value):
        cv.circle(frame, location_point , 0, color, 10)
    
    @staticmethod
    def draw_line(frame, from_xy, to_xy, data_text, color = Colors.RED.value):
        cv.line(frame,
                from_xy,
                to_xy,
                color,
                7)
        cv.putText(frame, 
                data_text,
                (to_xy[0] , to_xy[1]),
                2, 
                0.7, 
                (0, 255, 0)) # Green
        
    @staticmethod
    def draw_data(frame, text_data, location ,color = Colors.GREEN.value):
        cv.putText(frame, text_data, location, cv.FONT_HERSHEY_SIMPLEX, 1, color, 3)
