from django import forms
from .models import ArtWorks

class ArtWorksForm(forms.ModelForm):
    class Meta:
        model = ArtWorks
        fields = ['category', 'title', 'comment', 'image1', 'image2', 'image3', 'image4',
                  'image5', 'image6', 'image7', 'image8', 'image9', 'image10']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(field, forms.ImageField):
                field.widget = forms.widgets.ImageWidget()
