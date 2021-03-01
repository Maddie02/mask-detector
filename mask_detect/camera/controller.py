import cv2, os
from camera.camera import Camera
from threading import Thread
from django.core.mail import send_mail
from datetime import datetime, timezone, timedelta
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from accounts.models import Employee
from stats.models import Statistic
from django.shortcuts import redirect
import face_recognition
import time

WAIT_MINUTES = 0.5
VIOLATION_NUMBER = 3

MEDIA_FOLDER = '../mask_detect/media/profilepics/'

utc = timezone(offset=timedelta(hours=2))

class CameraThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.camera = Camera()

    def run(self):
        run_camera(self.camera)


def run_camera(camera):
    time.sleep(5)

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
                user = recognize_user(frame)

                if user:
                    if last_seen_without_mask == 0:
                        last_seen_without_mask = time.time()
                    
                    if (time.time() - last_seen_without_mask) / 60 >= WAIT_MINUTES:    
                        last_seen_without_mask = time.time()
                        times_caught_without_mask += 1
                        send_alert_mail(user, datetime.now(utc), times_caught_without_mask)

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


def recognize_user(frame):
    profile_pictures = []
    profile_pictures_path = os.listdir(MEDIA_FOLDER)

    for p_pic_path in profile_pictures_path:
        current_pic = os.path.join(MEDIA_FOLDER, p_pic_path)
        profile_pictures.append(current_pic)
    
    encode_frame = face_recognition.face_encodings(frame)[0] if len(face_recognition.face_encodings(frame)) != 0 else []

    if len(encode_frame) == 0:
        return

    for p_pic_path in profile_pictures:
        profile_pic = face_recognition.load_image_file(str(p_pic_path))
        profile_pic_encoding = face_recognition.face_encodings(profile_pic)[0]

        result = face_recognition.compare_faces([profile_pic_encoding], encode_frame)
        if result[0] == True:
            path = p_pic_path.partition("mask_detect/media/")[2]
            employee = Employee.objects.filter(profile_pic=path)

            if len(employee) == 0:
                return
            else:
                return employee.first()


def send_alert_mail(user, last_seen, repeat=None):

    additional_message = ''

    if repeat and repeat % VIOLATION_NUMBER == 0:
        create_stats(user, last_seen)
        additional_message = f'<span style="font-size:20px;">You were caught without a mask for the {repeat} time today!</span> <br>'

    message = f'''
        Hello, {user.first_name} {user.last_name},
        \n\n
        The Mask Detector caught you not wearing a mask at {last_seen.strftime("%H:%M:%S, %d/%m/%Y")}. 
        \n\n
        Please, wear your mask and stay safe!
        \n\n
        With love,\n
        The Mask Detector Team
    '''

    html_message = f'''
        Hello, {user.first_name} {user.last_name},
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
        [user.email],
        fail_silently=False,
        html_message=html_message
    )


def create_stats(user, last_seen):

    try:
        stat = Statistic.objects.filter(employee=user).first()
        if stat == None:
            stat = Statistic(employee=user, count_violations=1, last_seen_date=last_seen)
        else:
            stat.last_seen_date = last_seen
            stat.count_violations = stat.count_violations + 1
        stat.save()
    except:
        print("Error while creating/updating statistics")


