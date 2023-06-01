from django.test import override_settings

common_settings = override_settings(
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage',
)