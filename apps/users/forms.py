from datetime import date, timedelta
from django import forms

from apps.gym.models import GymSession, Plan
from .models import User


class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                    label="Номер телефона")
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                    label="Имя")
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                    label="Фамилия")
    plan = forms.ModelChoiceField(queryset=Plan.objects.all(), required=True,
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    label="План")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                                            'type': 'date',
                                                            'format': 'dd/mm/yyyy'}), label='Дата начала')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                                            'type': 'date',
                                                            'format': 'dd/mm/yyyy'}), label='Дата окончания')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'plan', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_date'].initial = date.today()

        thirty_days_later = date.today() + timedelta(days=30)
        self.fields['end_date'].initial = thirty_days_later


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