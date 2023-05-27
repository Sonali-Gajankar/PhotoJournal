from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import pagination, generics

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
    # template_name = "journal/user_home.html"
    ordering = ['-date']

    def get_template_names(self):
        if PhotoJournal.objects.filter(user=self.request.user):
            return "journal/user_photos.html"
        return "journal/user_home.html"


class UploadPhotoView(LoginRequiredMixin, generic.CreateView):
    model = PhotoJournal
    template_name = "journal/upload_photo.html"
    # fields = ["title", "description", "date", "photo"]
    form_class = UserPhotos

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UploadPhotoView, self).form_valid(form)


class DeletePhotoView(LoginRequiredMixin, generic.DeleteView):
    model = PhotoJournal
    context_object_name = "post"
    success_url = reverse_lazy("user_home")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class CursorPaginationPage(pagination.CursorPagination):
    page_size = 5
    page_size_query_param = "page_size"
    ordering = ["-date", "-id"]


class FetchImagesView(LoginRequiredMixin, generics.ListAPIView):
    queryset = PhotoJournal.objects.all()
    serializer_class = PhotoSerializer
    pagination_class = CursorPaginationPage
