from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.db import models
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import pagination, generics, permissions

from users.models import CustomUser
from .models import PhotoJournal
from .forms import UserPhotos
from .serializer import PhotoSerializer


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect("user_home")
    return render(request, "journal/home.html")


class UserHomeView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    model = PhotoJournal
    form_class = UserPhotos
    context_object_name = "photo_list"
    # template_name = "journal/user_home.html"
    ordering = ['-date']

    def get_template_names(self):
        if PhotoJournal.objects.filter(user=self.request.user):
            return "journal/user_photos.html"
        return "journal/user_home.html"

    def get_queryset(self):
        return PhotoJournal.objects.filter(user=self.request.user).order_by('-date')


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

    @receiver(models.signals.post_delete, sender=PhotoJournal)
    def remove_file_from_s3(sender, instance, using, **kwargs):
        instance.photo.delete(save=False)


class UpdatePhotoView(LoginRequiredMixin, generic.UpdateView):
    model = PhotoJournal
    template_name = "journal/upload_photo.html"
    form_class = UserPhotos
    context_object_name = "update_data"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdatePhotoView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdatePhotoView, self).get_context_data(**kwargs)
        context["page_type"] = "Update"
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    @receiver(models.signals.pre_save, sender=PhotoJournal)
    def remove_old_file_from_s3(sender, instance, created=False, **kwargs):
        if instance.pk:
            old_img = PhotoJournal.objects.get(pk=instance.pk)
            if old_img and old_img.photo.url != instance.photo.url:
                old_img.photo.delete(save=False)


class CursorPaginationPage(pagination.CursorPagination):
    page_size = 5
    page_size_query_param = "page_size"
    ordering = ["-date", "-id"]


class FetchImagesView(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = PhotoSerializer
    pagination_class = CursorPaginationPage
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PhotoJournal.objects.all().filter(user=self.request.user)