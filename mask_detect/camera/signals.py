from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from camera.controller import CameraThread

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    camera_thread = CameraThread(user)
    camera_thread.setDaemon(True)
    camera_thread.start()

