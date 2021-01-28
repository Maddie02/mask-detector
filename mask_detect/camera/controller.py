import cv2
from camera.camera import Camera
from threading import Thread
from django.core.mail import send_mail
from mask_detect.settings import EMAIL_HOST_USER
import time

class CameraThread(Thread):

    def __init__(self, user):
        Thread.__init__(self)
        self.user = user

    def run(self):
        camera = Camera()
        run_camera(self.user, camera)


def run_camera(user, camera):
    while camera.video.isOpened():
        success, frame = camera.get_frame()

        if success == False:
            continue

        (locs, preds) = camera.detect_and_predict_mask(frame)

        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, without_mask) = pred

            label = "Mask" if mask > without_mask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            
            # Send email to user and do other stuff if he's not wearing a mask
            if label == "No Mask":
                pass

            label = f'{label}: {(max(mask, without_mask) * 100):.2f}%'

            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    camera.release()


def send_alert_mail(email):
    send_mail(
        "Mask Detector Alert",
        "The Mask Detector caught you not wearing a mask. Please wear your mask and be safe!",
            "Mask Detector",
            [email],
            fail_silently=False
    )