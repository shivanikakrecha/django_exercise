import uuid
from django.db import models
from datetime import datetime


# Create your models here.
def get_mediafile_upload_to(instance, filename):
    """
    Generates the upload path for the FileField of UploadedImage model.

    Args:
        instance (UploadedImage): The UploadedImage instance being uploaded.
        filename (str): The original filename of the uploaded file.

    Returns:
        str: The formatted upload path for the file.
    """
    user_ip = instance.uploader_ip
    current_date = datetime.now().date()
    return f"uploaded_images/{user_ip}/{current_date}/{filename}"


class UploadedImage(models.Model):
    """
    Model representing an uploaded image with relevant metadata.
    """

    image = models.FileField(upload_to=get_mediafile_upload_to)
    upload_date = models.DateTimeField(auto_now_add=True, editable=False)
    uploader_ip = models.GenericIPAddressField()
    unique_identifier = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )

    class Meta:
        ordering = ["-upload_date"]
        verbose_name_plural = "Uploaded Images"

    def __str__(self):
        return f"Image {self.unique_identifier}"

    @classmethod
    def get_quota_remaining(cls, ip_address):
        """
        Calculates the remaining quota for image uploads for a given IP address on the current day.

        Args:
            ip_address (str): The IP address of the uploader.

        Returns:
            int: The number of remaining uploads allowed for the IP address on the current day.
        """
        today = datetime.now().date()
        uploads_today = cls.objects.filter(
            uploader_ip=ip_address, upload_date__date=today
        ).count()
        return max(10 - uploads_today, 0)

    def delete(self, *args, **kwargs):
        """
        Overrides the delete method to ensure the associated image file is deleted from storage.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.image.delete()
        super().delete(*args, **kwargs)
