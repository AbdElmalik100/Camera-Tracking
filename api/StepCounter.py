from .utils import Visualizer
import random
class StepCounter:
    """
    Counitng steps for selected person.
    also you can calculate the distance he walked.
    Attributes:
    Constants:
        Depending on YOLO pose estimation models, the IDs of the legs are as below
        LEFT_LEG_ID = 16
        RIGHT_LEG_ID = 15
        steps_data: dict = The dictionary that contains the steps for each person (Each ID).
    """
    def __init__(self) -> None:
        self.__LEFT_LEG_ID = 16
        self.__RIGHT_LEG_ID = 15
        self.steps_data = {}
        
    
    def steps_counter(self, frame, tracked_person_id:int, keypoints, ids, keep_every:int = 5, draw_pose:bool = True) -> any:
        """
        Parameters:
            frame = The frame of the video to modify it and show the steps.
            tracked_person_id : int = The ID of the person you want to count the steps.
            keypoints = The keypoints of the person you want to count the steps.
            ids = The detected ids so you can filter later.
            keep_every: int (default = 5) = To avoid overcounting, only count every `n` of steps.
            draw_pose: bool (default = True) = To draw the pose of the person.
            show_distance: bool (default = True) = To show the distance you walked (in meters).
        Return:
            frame = The frame of the video with the steps drawn on it.
            steps = The number of steps of the given ID person.
        """
        # Getting Id old steps_data
        if tracked_person_id not in self.steps_data.keys():
            self.steps_data[tracked_person_id] = []
        if ids is None or keypoints is None: return frame, 0
        for person_id, person_keypoints in zip(ids, keypoints):
            
            if len(person_keypoints) == 0: break
            left_leg_cordinates = person_keypoints[self.__LEFT_LEG_ID]
            right_leg_cordinates = person_keypoints[self.__RIGHT_LEG_ID]
            
            # TODO For testing propose           
            if person_id.item() == ids[0]:
            # if person_id.item() == tracked_person_id: # Counting for only for tracked person.
                frame = self.__draw_pose(frame, left_leg_cordinates, right_leg_cordinates) if draw_pose else frame
                
                if random.randint(1,keep_every) == 1: # Avoid overcounting and only count every `n` of steps.
                    self.__add_legs_coordinates_sub(tracked_person_id, left_leg_cordinates[0], right_leg_cordinates[0]) # 0 : horizontal, 1 : vertical


        steps = self.cal_id_steps(tracked_person_id)
        Visualizer.draw_data(frame, str(steps) + " Step", (550, 30))
        
        distance = self.__calculate_distance(steps)
        Visualizer.draw_data(frame, str(round(distance, 2)) + " Meters", (550, 60))
            
        return frame, steps, distance
        
    def __add_legs_coordinates_sub(self, person_id:int, left_leg_cordinates:int , right_leg_cordinates:int) -> None:
        """
        Substracting the coordinates of the left and right legs. and adding them to the steps_data dictionary of the given ID.
        Parameters:
            person_id : int = The ID of the person.
            left_leg_cordinates : int = The coordinates of the left leg.
            right_leg_cordinates : int = The coordinates of the right leg.
        """
        person_previous_steps = self.steps_data[person_id]
        person_previous_steps.append((right_leg_cordinates - left_leg_cordinates))
        self.steps_data[person_id] = person_previous_steps
            
    def cal_id_steps(self, person_id:int) -> int:
        """
        Calculating Steps of a given Id.
        Parameters:
            person_id : int = The ID of the person.
        Return:
            steps : int = The number of steps of the given ID person.
        """
        person_steps_data = self.steps_data[person_id]
        steps = 0
        for i in range(1, len(person_steps_data)):
            # Sign change of steps_data is counted as a step
            if (person_steps_data[i] < 0 and person_steps_data[i-1] >= 0) or (person_steps_data[i] >= 0 and person_steps_data[i-1] < 0):
                steps += 1
                
        return steps
    
    def __calculate_distance(self, steps, average_step_size:float = 5):
        """
        Calculating the distance you walked (in meters), using the average step size.
        Parameters:
            steps : int = The number of steps you walked.
            average_step_size : float (default = 5) = The average step size you walked. (in miles/hour)
        """

        return steps * 0.3048 * average_step_size  # Steps * feet_to_meters * average_step_size
    
    def __draw_pose(self, frame, left_leg_cordinates, right_leg_cordinates):
        """
        Drawing the pose estimation of the person.
        Parameters:
            frame = The frame of the video to modify it and show the steps.
            left_leg_cordinates = The coordinates of the left leg.
            right_leg_cordinates = The coordinates of the right leg.
        Return:
            frame = The frame of the video with the steps drawn on it.
        """
        Visualizer.draw_point(frame, (int(left_leg_cordinates[0]),int(left_leg_cordinates[1])))
        Visualizer.draw_point(frame, (int(right_leg_cordinates[0]),int(right_leg_cordinates[1])))
        return frame
