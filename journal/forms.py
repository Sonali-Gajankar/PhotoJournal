from django.forms import ModelForm, widgets
from .models import PhotoJournal


class UserPhotos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs.update({"id": "img__upload_field"})
        self.fields["description"].widget.attrs.update({"class": "description", "rows": "1"})
        self.fields["title"].widget.attrs.update({"class": "title"})
        self.fields["date"].widget.attrs.update({"id": "date"})

    class Meta:
        model = PhotoJournal
        fields = ["title", "description", "date", "photo"]
        widgets = {'date': widgets.DateInput(
            attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'})}

