from django.apps import AppConfig
from threading import Thread
from camera.views import CameraThread


class CameraConfig(AppConfig):
    name = 'camera'

    def ready(self):
        CameraThread().start()
