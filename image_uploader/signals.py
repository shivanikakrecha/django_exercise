from django.db.models.signals import pre_save
from django.dispatch import receiver
from image_uploader.models import UploadedImage
from django.core.exceptions import ValidationError
from django.conf import settings


@receiver(pre_save, sender=UploadedImage)
def check_image_upload_quota_exceeded(sender, instance, **kwargs):
    """
    Signal receiver function to check if the IP address has reached the daily
    quota before saving the image.

    Arguments:
        sender (Model): The model class that sends the signal.
        instance (UploadedImage): The instance of UploadedImage being saved.
        **kwargs: Additional keyword arguments.

    Raises:
        ValidationError: If the upload quota for the uploader's IP has been
        exceeded for the day.

    Returns:
        UploadedImage: The instance of UploadedImage if the quota is not
        exceeded.
    """
    quota_remaining = instance.get_quota_remaining(instance.uploader_ip)

    # Check if the remaining quota exceeds the maximum allowed image upload
    if quota_remaining > settings.MAX_ALLOWED_IMAGE_UPLOAD:
        raise ValidationError("Upload quota for this IP has been exceeded for the day.")
    else:
        return instance
