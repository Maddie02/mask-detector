import cv2
from camera.camera import Camera
from threading import Thread
from django.core.mail import send_mail
from mask_detect.settings import EMAIL_HOST_USER
from datetime import datetime, timezone, timedelta
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

WAIT_MINUTES = 5.0
utc = timezone(offset=timedelta(hours=2))

class CameraThread(Thread):

    def __init__(self, user):
        Thread.__init__(self)
        self.user = user

    def run(self):
        camera = Camera()
        run_camera(self.user, camera)


def run_camera(user, camera):
    last_seen_without_mask = 0
    times_caught_without_mask = 0

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
            
            if label == "No Mask":
                employee_name = user.first_name + ' ' + user.last_name

                if last_seen_without_mask == 0:
                    last_seen_without_mask = datetime.now(utc)
                    times_caught_without_mask += 1
                    send_alert_mail(employee_name, user.email, last_seen_without_mask, repeat=times_caught_without_mask)
                    continue
                
                time_interval = datetime.now(utc) - last_seen_without_mask

                if time_interval.total_seconds() / 60 >= WAIT_MINUTES:
                    last_seen_without_mask = datetime.now(utc)
                    times_caught_without_mask += 1
                    send_alert_mail(employee_name, user.email, last_seen_without_mask, repeat=times_caught_without_mask)
            else:
                last_seen_without_mask = 0
            
            label = f'{label}: {(max(mask, without_mask) * 100):.2f}%'

            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    camera.release()


def send_alert_mail(name, email, last_seen, repeat=None):

    additional_message = ''

    if repeat and repeat % 5 == 0:
        additional_message = f'<span style="font-size:20px;">You were caught without a mask for the {repeat}th time today!</span> <br>'

    message = f'''
        Hello, {name},
        \n\n
        The Mask Detector caught you not wearing a mask at {last_seen.strftime("%H:%M:%S, %d/%m/%Y")}. 
        \n\n
        Please, wear your mask and stay safe!
        \n\n
        With love,\n
        The Mask Detector Team
    '''

    html_message = f'''
        Hello, {name},
        <br> <br>
        The Mask Detector caught you not wearing a mask at {last_seen.strftime("%H:%M:%S, %d/%m/%Y")}. 
        <br>
        <p>
            {additional_message}<strong>Please, wear your mask and stay safe!</strong>
        </p>
        <br>
        With love,<br>
        The Mask Detector Team
    '''

    send_mail(
        "Mask Detector Alert",
        message,
        "Mask Detector",
        [email],
        fail_silently=False,
        html_message=html_message
    )

