from django.urls import path
from .views import home, UserHomeView, UploadPhotoView, FetchImagesView, DeletePhotoView, UpdatePhotoView

urlpatterns = [
    path('', home, name='home'),
    path('user-home/', UserHomeView.as_view(), name='user_home'),
    path('user-home/<int:pk>/delete/', DeletePhotoView.as_view(), name='delete_pic'),
    path('user-home/update/<int:pk>/', UpdatePhotoView.as_view(), name='update_pic'),
    path('upload-photo/', UploadPhotoView.as_view(), name='upload_photo'),
    path('fetch-photos/', FetchImagesView.as_view()),
]