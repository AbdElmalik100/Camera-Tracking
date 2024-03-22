import cv2 as cv
import mediapipe as mp

class FaceDetector:
    def __init__(self, min_detection_confidence = 0.7, model_selection = 0):
        self.face_detector = mp.solutions.face_detection.FaceDetection(min_detection_confidence=min_detection_confidence,model_selection=model_selection)
        
    def detect(self, detected_person,previous_face_width, person_id):
        detection = self.face_detector.process(detected_person.astype('uint8'))
        
        if detection.detections:
            for detection in detection.detections:
                h, w, c = detected_person.shape
                bboxC = detection.location_data.relative_bounding_box # Bounding Box Class
                bbox = int(bboxC.xmin * w) , int(bboxC.ymin * h) , int(bboxC.width * w) , int(bboxC.height * h)
                
                # Drawing Bounding Box
                detected_person = cv.rectangle(detected_person , bbox , (255,0,255) , 2)
                
                if previous_face_width < bboxC.width * w:
                    detected_face = detected_person[int(bboxC.ymin * h):int(bboxC.ymin * h)+int(bboxC.height * h) ,int(bboxC.xmin * w):int(bboxC.xmin * w)+ int(bboxC.width * w)]
                    cv.imwrite(f"Detected Faces/{person_id}.jpg",detected_face)
                    
                    return detected_face
                
        return None
