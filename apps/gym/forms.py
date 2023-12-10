from datetime import date, timedelta
from django import forms

from apps.gym.models import Plan, Subscription
from apps.users.models import User


class AddSubscriptionForm(forms.ModelForm):
    member = forms.ModelChoiceField(queryset=User.objects.all(), required=True,
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    label="Пользователь")
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
        model = Subscription
        fields = ['member', 'plan', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_date'].initial = date.today()

        thirty_days_later = date.today() + timedelta(days=30)
        self.fields['end_date'].initial = thirty_days_later