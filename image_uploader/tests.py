from django.test import TestCase
import uuid
from .models import UploadedImage
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime


class UploadImageTestCase(TestCase):
    def setUp(self) -> None:
        image = SimpleUploadedFile(
            "test_image.jpg", b"image_content", content_type="image/jpeg"
        )
        created_image = UploadedImage.objects.create(
            image=image,
            upload_date=datetime.now(),
            uploader_ip="127.0.0.1:8000",
            unique_identifier=uuid.uuid4,
        )
        return super().setUp()
