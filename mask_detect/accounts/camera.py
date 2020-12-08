import cv2, os
from keras.models import load_model

current_path = os.path.abspath(".")
path_to_model = os.path.join(current_path, "../ai/", "face-mask-detector.h5")


def load_face_detector():
    print("Loading face detector model...")
    try:
        prototxt_file_path = os.path.join(current_path, "accounts/face-detect", "deploy.prototxt.txt")
        weights_path =  os.path.join(current_path, "accounts/face-detect", "res10_300x300_ssd_iter_140000.caffemodel")
        print("Face detector model succesfully loaded!")
        
    except Exception as e:
        print("Error while loading face detector pre-trained model.", e)

    face_net = cv2.dnn.readNet(prototxt_file_path, weights_path)
    return face_net


def load_face_mask_detector():

    print("Loading face mask detector model...")

    try:
        model = load_model(path_to_model)
    
    except Exception as e:
        print("Error while loading face mask detector.", e)
    
    return model


def camera_processing(face_detector, face_mask_detector):
    stream = cv2.VideoCapture(0)

    while True:
        ret, frame = stream.read()

        # Process data and make predictions

        key = cv2.waitKey(1)

        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()
    stream.release()


face_detector = load_face_detector()
face_mask_detector = load_face_mask_detector()

camera_processing(face_detector, face_mask_detector)