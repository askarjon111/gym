from django import forms

from apps.gym.models import Plan
from .models import User


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
