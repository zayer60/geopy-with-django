from django import forms
from .models import Measurement

class DistanceForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('destination',)