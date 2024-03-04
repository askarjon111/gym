from datetime import date, timedelta
from django import forms
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from apps.gym.models import GymSession, Plan
from .models import User, UserProfile


class UserCreateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   label="Номер телефона")
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label="Имя")
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label="Фамилия")
    # plan = forms.ModelChoiceField(queryset=Plan.objects.filter(is_active=True), required=True,
    #                               widget=forms.Select(
    #                                   attrs={'class': 'form-control'}),
    #                               label="План")
    # start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
    #                                                            'type': 'date',
    #                                                            'format': 'dd/mm/yyyy'}), label='Дата начала')
    # end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
    #                                                          'type': 'date',
    #                                                          'format': 'dd/mm/yyyy'}), label='Дата окончания')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


class UserUpdateForm(forms.Form):
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control'}), label="Номер телефона")
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}), label="Имя")
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}), label="Фамилия")


    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['phone_number'].initial = self.instance.phone_number
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name


    def save(self, commit=True):
        if self.instance:
            self.instance.phone_number = self.cleaned_data['phone_number']
            self.instance.first_name = self.cleaned_data['first_name']
            self.instance.last_name = self.cleaned_data['last_name']
            if commit:
                self.instance.save()
            return self.instance
        return None


class UserProfileCreateForm(forms.ModelForm):
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                              label="Вес")
    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                              label="Рост")
    biceps = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                              label="Бицепс")
    triceps = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                               label="Трицепс")
    chest = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                             label="Грудь")
    guts = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                            label="Живот")
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                                       label="Фото профиля")
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES,
                               widget=forms.Select(
                                   attrs={'class': 'form-control'}),
                               label="Пол")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                                                  'type': 'date',
                                                                  'format': 'dd/mm/yyyy'}),
                                    label='Дата рождения')
    # user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES,
    #                               widget=forms.Select(
    #                                   attrs={'class': 'form-control'}),
    #                               label="Тип пользователя")

    class Meta:
        model = UserProfile
        fields = ('weight', 'height', 'biceps', 'triceps', 'chest', 'guts', 'profile_picture',
                  'gender', 'date_of_birth', 'user_type')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.request.user
        if user:
            profile.user = user
            profile.save()
        return profile


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = GymSession
        fields = ['member', 'start']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = forms.HiddenInput()

    def save(self, commit=True, **kwargs):
        instance = super(AttendanceForm, self).save(commit=False)
        instance.start = kwargs.get('start', None)
        try:
            if commit:
                instance.save()
        except ValueError:
            messages.add_message(request=self.request,
                                 level=messages.ERROR,
                                 message="У участника нет действующего действующего плана подписки.")
            return redirect('users')
        return instance


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone_number', 'first_name',
                  'last_name', 'password1', 'password2']
