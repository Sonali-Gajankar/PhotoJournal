from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import views, status
from rest_framework import permissions
from rest_framework.response import Response

from .models import PhotoJournal
from .forms import UserPhotos
from .serializer import PhotoSerializer


# Create your views here.

def home(request):
    return render(request, "journal/home.html")


class UserHomeView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = PhotoJournal
    form_class = UserPhotos
    context_object_name = "photo_list"
    template_name = "journal/user_home.html"
    ordering = ['-date']


class UploadPhotoView(LoginRequiredMixin, generic.CreateView):
    model = PhotoJournal
    template_name = "journal/upload_photo.html"
    # fields = ["title", "description", "date", "photo"]
    form_class = UserPhotos

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UploadPhotoView, self).form_valid(form)

    def test_func(self):
        self.request


class GetImagesView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        photos = PhotoJournal.objects.filter(user=request.user.id)
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
