import cv2 as cv
from ultralytics.solutions import heatmap, speed_estimation, distance_calculation

class YOLOTools:
    """
    A bunch of YOLO Tools 
    Note that maybe you would like to keep the order to avoid the overlapping.
    * Distance Estimation
    * Speed Estimation
    * Heatmap
    """
    
    @staticmethod
    def heatmap(vid_width:int, vid_height:int,view_img:bool = False) -> any:
        """
        Creating a heatmap object. 
        Note That you have update the frame with the YOLO Heatmap output to see the updated frame
        Parameters:
            vid_width: int = width of the video
            vid_height: int = height of the video
            view_img: bool (default = False)= if you want to show YOLO frames.
        """
        heatmap_obj = heatmap.Heatmap()
        heatmap_obj.set_args(colormap=cv.COLORMAP_PARULA,
                            imw=vid_width,
                            imh=vid_height,
                            view_img=view_img,
                            shape="circle",
                            )
        return heatmap_obj
    
    @staticmethod
    def speed_estimation(classes: list, line_points: list, view_img:bool = False) -> any:
        """
        Calculating the speed of boxes when passes through the line.
        Parameters:
            classes: list = list of class names.
            line_points: list = list of points of the lines to calculate the speed.
            view_img: bool (default = False)= if you want to show YOLO frames.
        """
        speed_obj = speed_estimation.SpeedEstimator()
        speed_obj.set_args(reg_pts=line_points,
                           names=classes,
                           view_img=view_img,
                           )
        return speed_obj
    
    @staticmethod
    def distance_calculation(classes: list, view_img:bool = True) -> any:
        """
        Calcualting the distance between to selected boxes using an interacitve window.
        Note that actions like selecitng two points to calculate the distance working only when you use 
        the view_img of YOLO8
        Parameters:
            classes: list = list of class names.
            view_img: bool (default = False)= if you want to interact and selecting boxes.
        """
        dist_obj = distance_calculation.DistanceCalculation()
        dist_obj.set_args(names=classes, view_img=view_img)
        return dist_obj
