from django import forms
from .models import UploadImage
from crispy_forms.helper import FormHelper

class UploadImageForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = True

    class Meta:
        model = UploadImage
        fields = [
            'images',
        ]
