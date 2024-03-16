from django import forms

from apps.controls.models import Gym
from apps.users.models import User
from .models import Notification


class NotificationForm(forms.ModelForm):
    gym = forms.ModelChoiceField(queryset=Gym.objects.all(), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}), label="Спортзал")
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label="Заголовок")
    body = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label="Текст")
    send_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control',
                                                                    'type': 'datetime-local'}),
                                  label="Время отправки")
    type = forms.ChoiceField(widget=forms.Select(choices=Notification.TYPE_CHOICES,
                                                 attrs={'class': 'form-control'}),
                             label="Отправить через", choices=Notification.TYPE_CHOICES)

    class Meta:
        model = Notification
        fields = ['title', 'body', 'send_at', 'type', 'gym']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.instance = kwargs.pop('instance', None)
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.instance.gym = self.request.user.gym
        self.fields['gym'].widget = forms.HiddenInput()
        self.fields['send_at'].widget = forms.widgets.DateTimeInput(
            attrs={'type': 'datetime-local'})
        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['body'].initial = self.instance.body
            self.fields['send_at'].initial = self.instance.send_at
            self.fields['type'].initial = self.instance.type

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance:
            self.fields['title'].initial = self.cleaned_data['title']
            self.fields['body'].initial = self.cleaned_data['body']
            self.fields['send_at'].initial = self.cleaned_data['send_at']
            self.fields['type'].initial = self.cleaned_data['type']
            if commit:
                self.instance.save()
            return self.instance
        return instance
