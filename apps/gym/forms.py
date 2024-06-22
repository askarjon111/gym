from datetime import timedelta
from django.utils import timezone
from django import forms
from apps.controls.models import Gym

from apps.gym.models import GymEquipment, Plan, Subscription
from apps.users.models import User


class AddSubscriptionForm(forms.ModelForm):
    member = forms.ModelChoiceField(queryset=User.objects.all(), required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control'}),
                                    label="Пользователь")
    plan = forms.ModelChoiceField(queryset=Plan.objects.filter(is_active=True), required=True,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control'}),
                                  label="План")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                                               'type': 'date'}, format="%Y-%m-%d"))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control',
                                                             'type': 'date'}, format="%Y-%m-%d"))

    class Meta:
        model = Subscription
        fields = ['member', 'plan', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.is_authenticated:
            self.fields['plan'].queryset = Plan.objects.filter(
                gym=self.request.user.gym, is_active=True)
            self.fields['member'].queryset = Gym.objects.get_members(
                self.request.user.gym.id)

            self.fields['start_date'].initial = timezone.now()
            thirty_days_later = timezone.now() + timedelta(days=31)
            self.fields['end_date'].initial = thirty_days_later


class AddNewPlanForm(forms.ModelForm):
    gym = forms.ModelChoiceField(queryset=Gym.objects.all(), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}), label="Спортзал")
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label="Название")
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  label="Описание")
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Цена (сум)")
    sessions = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Сессии (оставьте 0 для VIP-сессий)")
    days = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Продолжительность (днях)")

    class Meta:
        model = Plan
        fields = ['gym', 'name', 'description', 'price', 'sessions', 'days']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.gym = kwargs.pop('gym', None)
        super().__init__(*args, **kwargs)
        super(AddNewPlanForm, self).__init__(*args, **kwargs)
        self.fields['gym'].widget = forms.HiddenInput()


    def save(self, commit=True, **kwargs):
        instance = super(AddNewPlanForm, self).save(commit=False)
        if not instance.pk:
            instance.gym = self.gym

        instance.save()


class AddNewGymEquipmentForm(forms.ModelForm):
    gym = forms.ModelChoiceField(queryset=Gym.objects.all(), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}), label="Спортзал")
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label="Название")
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  label="Описание")
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), label="Изображение")

    class Meta:
        model = GymEquipment
        fields = ['gym', 'name', 'description', 'image']


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.gym = kwargs.pop('gym', None)
        super().__init__(*args, **kwargs)
        self.fields['gym'].widget = forms.HiddenInput()


    def save(self, commit=True, **kwargs):
        instance = super(AddNewGymEquipmentForm, self).save(commit=False)
        if not instance.pk:
            instance.gym = self.gym

        instance.save()
