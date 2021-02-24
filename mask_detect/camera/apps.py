from django.apps import AppConfig
from threading import Thread


class CameraConfig(AppConfig):
    name = 'camera'

    def ready(self):
        from camera.controller import CameraThread

        camera_thread = CameraThread()
        camera_thread.setDaemon(True)
        camera_thread.start()
