from django.shortcuts import render, redirect
from .forms import CityForm
from .models import City
from django.contrib import messages
import requests

# Create your views here.

def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},&appid=b7a87cee3d8a35991d25082cfb0cfcd4&units=metric'

    if request.method=='POST':
        form=CityForm(request.POST)
        if form.is_valid():
            NCity=form.cleaned_data['name']
            CCity=City.objects.filter(name=NCity).count()
            if CCity==0:
                res=requests.get(url.format(NCity)).json()
                if res['cod']==200:
                    form.save()
                    messages.success(request, " "+NCity+" City Added Successfully...!!!")
                else:
                    messages.error(request, "City Does Not Exists...!!!")
            else:
                messages.error(request, " "+NCity+" City Already Exists...!!!")

    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:
        res=requests.get(url.format(city)).json()
        city_weather = {
            'city' : city,
            'temperature' : res['main']['temp'],
            'description' : res['weather'][0]['description'],
            'country' : res['sys']['country'],
            'icon' : res['weather'][0]['icon'],
        }
        data.append(city_weather)
    return render(request, "weatherapp.html",{'form':form,'data':data})


def delete_city(request, CName):
    c=City.objects.get(name=CName)
    c.delete()
    messages.success(request, " "+CName+" City Deleted Successfully...!!!")
    return redirect('home')