from django.views.generic import View, CreateView, DetailView, DeleteView
from django.http import JsonResponse
from datetime import datetime
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import UploadedImage
from .forms import UploadedImageForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ImageUploadView(LoginRequiredMixin, CreateView):
    """The view for uploading images using a form"""

    model = UploadedImage
    login_url = "login/"
    template_name = "image_uploader/image_upload.html"
    form_class = UploadedImageForm

    def form_valid(self, form):
        # Check if the IP has exceeded the daily quota
        ip = self.request.META.get("REMOTE_ADDR")

        # Save the image and insert uploader_ip
        form.instance.uploader_ip = ip

        # Call the parent class method to handle form validation
        response = super().form_valid(form)

        return response

    def get_success_url(self):
        # Redirect to the detail page of the uploaded image using its unique identifier
        return reverse_lazy(
            "image_uploader:image-detail",
            kwargs={"unique_identifier": self.object.unique_identifier},
        )


class ImageDetailView(LoginRequiredMixin, DetailView):
    """
    Display details of an uploaded image.

    Identify object based on the "unique_identifier" and display
    required details on the detail page.
    """

    model = UploadedImage
    login_url = "login/"
    template_name = "image_uploader/image_detail.html"
    context_object_name = "image"
    slug_url_kwarg = "unique_identifier"
    slug_field = "unique_identifier"


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = UploadedImage
    login_url = "login/"
    template_name = "image_uploader/image_delete.html"
    success_url = reverse_lazy("image_uploader:image_upload")
    slug_url_kwarg = "unique_identifier"
    slug_field = "unique_identifier"

    def delete(self, request, *args, **kwargs):
        """Raises PermissionDenied if the user is not allowed to delete the image.

        :param request: The HTTP request object.
        :param args: View arguments.
        :param kwargs: View keyword arguments containing the "unique_identifier" value.
        :raises PermissionDenied: If the user is not allowed to delete the image.
        :return: HTTP response after successful deletion.
        """
        image = self.get_object()
        if image.uploader_ip != request.META.get("REMOTE_ADDR"):
            raise PermissionDenied("You are not allowed to delete this image.")
        return super().delete(request, *args, **kwargs)
