from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'friends']  # Include both user and friends fields

        widgets = {
            'friends': forms.CheckboxSelectMultiple(),  # Allows multiple selections
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Check if the profile instance exists
            # Exclude the current user and already friends from the queryset
            self.fields['friends'].queryset = User.objects.exclude(pk=self.instance.user.pk).exclude(
                id__in=self.instance.friends.values_list('id', flat=True)
            )
        else:
            self.fields['friends'].queryset = User.objects.all()

    def clean_friends(self):
        friends = self.cleaned_data.get('friends')
        return friends