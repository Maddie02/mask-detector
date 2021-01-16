import cv2, os
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input

MIN_CONFIDENCE_DETECT = 0.5

class Camera:

    def __init__(self):
        self.face_detector = self.load_face_detector()
        self.face_mask_detector = self.load_face_mask_detector()

    # Load face detector model from OpenCV
    def load_face_detector(self):
        print("Loading face detector model...")
        try:
            prototxt_file_path = os.path.join(".", "./accounts/face-detect/", "deploy.prototxt.txt")
            weights_path =  os.path.join(".", "./accounts/face-detect/" "res10_300x300_ssd_iter_140000.caffemodel")
            print("Face detector model succesfully loaded!")
        except Exception as e:
            print("Error while loading face detector pre-trained model.", e)

        face_net = cv2.dnn.readNet(prototxt_file_path, weights_path)

        return face_net
    
    # Load custom face-mask detector
    def load_face_mask_detector(self):
        print("Loading face mask detector model...")
        try:
            path_to_face_mask_model = os.path.join(".", "../ai/", "face-mask-detector.h5")
            model = load_model(path_to_face_mask_model)
            print("Face Mask model succesfully loaded!")
        except Exception as e:
            print("Error while loading face mask detector.", e)
        
        return model
    
    # Make predictions for each frame
    def detect_and_predict_mask(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

        self.face_detector.setInput(blob)
        detections = self.face_detector.forward()

        faces = []
        locs = []
        preds = []

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > MIN_CONFIDENCE_DETECT:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                face = frame[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)

                faces.append(face)
                locs.append((startX, startY, endX, endY))
            
        if len(faces) > 0:
            faces = np.array(faces, dtype="float32")
            preds = self.face_mask_detector.predict(faces, batch_size=32)

        return (locs, preds)
    
    # Play the camera and process predictions
    def process(self):
        stream = cv2.VideoCapture(0)

        while True:
            ret, frame = stream.read()

            (locs, preds) = self.detect_and_predict_mask(frame)

            for (box, pred) in zip(locs, preds):
                (startX, startY, endX, endY) = box
                (mask, without_mask) = pred

                label = "Mask" if mask > without_mask else "No Mask"
                color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                label = f'{label}: {(max(mask, without_mask) * 100):.2f}%'

                cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)

            if key == ord('q'):
                break
        
        cv2.destroyAllWindows()
        stream.release()

