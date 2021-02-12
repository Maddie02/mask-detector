from django.apps import AppConfig
from threading import Thread


class CameraConfig(AppConfig):
    name = 'camera'

    def ready(self):
        import camera.signals
