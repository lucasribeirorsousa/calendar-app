from django import forms
from .models import Event
from pytz import all_timezones


TIMEZONE_CHOICES = [(tz, tz) for tz in all_timezones]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date', 'duration_days', 'duration_hours', 'recurring', 'recurrence_frequency', 'recurrence_end_date', 'timezone']

    timezone = forms.ChoiceField(
        choices=[('', 'Selecione um fuso horário')] + TIMEZONE_CHOICES,
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )

    duration_hours = forms.IntegerField(
        min_value=0, max_value=24, initial=0, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    recurring = forms.BooleanField(required=False)

    recurrence_frequency = forms.ChoiceField(
        choices=[('', 'Selecione uma opção'), ('daily', 'Diariamente'), ('weekly', 'Semanalmente'), ('monthly', 'Mensalmente')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    recurrence_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )