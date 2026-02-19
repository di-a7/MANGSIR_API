from django.apps import AppConfig


class RmsConfig(AppConfig):
    name = 'rms'
    
    def ready(self):
        import rms.signals
