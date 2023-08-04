from django.apps import AppConfig


class ImageUploaderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "image_uploader"

    def ready(self):
        from . import signals  # Import the signals module to register the signal
