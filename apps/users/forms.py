from django import forms
from django.contrib.auth.forms import AuthenticationForm

from apps.gym.models import GymSession, Plan
from .models import User

class CustomAuthenticationForm(AuthenticationForm):
    pass

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   label="Номер телефона")
    first_name = forms.CharField(max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                                    label="Имя")
    last_name = forms.CharField(max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                                    label="Фамилия")
    plan = forms.ModelChoiceField(queryset=Plan.objects.all(),
                                    required=True,
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    label="План")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'plan')


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = GymSession
        fields = ['member', 'start']

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = forms.HiddenInput()

    def save(self, commit=True, **kwargs):
        instance = super(AttendanceForm, self).save(commit=False)
        instance.start = kwargs.get('start', None)
        if commit:
            instance.save()
        return instance