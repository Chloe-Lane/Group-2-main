from django import forms
from django.core.exceptions import ValidationError

from .models import Tweet

class TweetModelForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content', 'user']

