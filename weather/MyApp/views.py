from django.shortcuts import render, redirect 
from .forms import CityForm
from .models import City
from django.contrib import messages
import requests

# Create your views here.

def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},&appid=b7a87cee3d8a35991d25082cfb0cfcd4&units=metric'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():         #cleaned_data is used to validated fieldss are stored..
            NCity=form.cleaned_data['name'] #forms.py la iruka field    #city name type panna use aagum
            CCity=City.objects.filter(name=NCity).count()       #ipo type panra city ah already type pannirunthom na db la store aagirum, ipo type pannathum already pannathum same iruntha 'count()=1' else part poi 'alreay exist' nu print aagum
            if CCity==0:
                res=requests.get(url.format(NCity)).json()    #namba type panna city openweatherapp la iruntha keela iruka nested if ku pogum illla na else part ku pogum -> json() format la athula than 'cad=200' irukkum
                #print(res)
                if res['cod']==200:    #ithu eathukkuna res la vara city openweatherapp la iruthan athoda 'cod'=200 nu irukkum, so atha form.save() la db save aagidum, type panra city illana else part run aagum 
                    form.save()                         #'cod=200' ah iruntha than save pani message show aagum....
                    messages.success(request, " "+NCity+" Added Successfully...!!!")
                else:
                    messages.error(request, "City Does Not Exists...!!!")
            else:
                messages.error(request, "City Already Exists...!!!")
                
    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:
        res=requests.get(url.format(city)).json()
        #print(res)
        city_weather={
            'city': city,
            'temperature' : res['main']['temp'],        #res nu eathukku use panrom na json format la irukka values eadukka use panrom
            'description' : res['weather'][0]['description'],
            'country' : res['sys']['country'],
            'icon' : res['weather'][0]['icon'],
        }
        data.append(city_weather)
    context={'data':data, 'form':form}
    return render(request, "weather.html",context)
    #return render(request, "weather.html",{'data':data, 'form':form})



"""
{'coord': {'lon': 80.2785, 'lat': 13.0878}, 
'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
'base': 'stations', 'main': {'temp': 34.06, 'feels_like': 41.06, 'temp_min': 32.99, 'temp_max': 35.03, 'pressure': 1005, 'humidity': 71, 'sea_level': 1005, 'grnd_level': 1004}, 
'visibility': 6000, 'wind': {'speed': 2.57, 'deg': 120}, 'clouds': {'all': 75}, 'dt': 1723617719,
 'sys': {'type': 2, 'id': 2093220, 'country': 'IN', 'sunrise': 1723595193, 'sunset': 1723640446}, 
'timezone': 19800, 'id': 1264527, 'name': 'Chennai', 'cod': 200}
"""

def delete_city(request, CName):
    #c=City.objects.get(name=CName)
    #c.delete()
    City.objects.get(name=CName).delete()
    messages.success(request, " "+CName+" Deleted Successfully...!!!")
    return redirect('home')