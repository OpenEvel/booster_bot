from django import forms
from django.db.models import fields
from django.forms import widgets

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',
        )
        widgets = {
            'name': forms.TextInput
        }