from django.urls import path
from .views import home, UserHomeView, UploadPhotoView, GetImagesView

urlpatterns = [
    path('', home, name='home'),
    path('user-home/', UserHomeView.as_view(), name='user_home'),
    path('upload-photo/', UploadPhotoView.as_view(), name='upload_photo'),
    path('get-photos/', GetImagesView.as_view()),
]