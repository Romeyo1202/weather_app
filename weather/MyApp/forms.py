#from django import forms
from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
#class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name':TextInput(attrs={'class':'form-control', 'placeholder':'City Name...'})}
        #widgets = {'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'City Name'})}