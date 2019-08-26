import requests
import json
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=7e182732b8c643a011c3a25e6818347a&units=metric'
    forcast = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=9592f34c6a983bfdb66810b0ea05cedb&units=metric'
    errormsg = ''
    msg = ''
    msg_class = ''
    

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            count = City.objects.filter(name=new_city).count()
            if count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:

                    form.save()
                else:
                    errormsg = 'This city does not exists!'
            else:
                errormsg = 'City already exists!'
        if errormsg:
            msg = errormsg
            msg_class = 'is-danger'
        else:
            msg = 'The city added successfully!'
            msg_class = 'is-success'
    form = CityForm()
    
    cities = City.objects.all()
    if cities.count() == 0:
        text = ''
        height = '100vh'
    else:
        text = 'Weather Forcasting'
        height = '100%'

    weather_data = []
    forcast_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        f = requests.get(forcast.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'cloud': r['clouds']['all'],
            'windspeed': r['wind']['speed'],

        }
        for i in range(25):

            forcast_dic = {
            'city' : city.name,
            'tem' : f['list'][i]['main']['temp'],
            'descript' : f['list'][i]['weather'][0]['description'],
            'date' : f['list'][i]['dt_txt'],
            'icon': f['list'][i]['weather'][0]['icon'],
            'cloudns' : f['list'][i]['clouds']['all'],
            'wind' : f['list'][i]['wind']['speed'],
            }
            forcast_data.append(forcast_dic)

        weather_data.append(city_weather)

    context = {'weather_data': weather_data,
               'form': form,
               'msg': msg,
               'msg_class': msg_class,
               'forcast_data': forcast_data,
               'text' : text,
               'height' : height
               }
    
    return render(request, 'weather_app/index.html', context)
    


def delete(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')




def location(request):

    loc_url = "http://api.ipstack.com/103.87.24.78?access_key=349062ce51620eb8e51bfe81f008aa3e"
    req = requests.get(loc_url)
    loc_json = req.json()
    city = loc_json['city']
    zip_code = loc_json['zip']
    country_code = loc_json['country_code']
    
    forc_url = 'http://api.openweathermap.org/data/2.5/forecast?zip={},{}&appid=0a4b36a876e547fd67992774e6fc1334&units=metric'
    

    url = 'http://api.openweathermap.org/data/2.5/weather?zip={},{}&appid=7ae7651349268c2c5448213db5f19e1b&units=metric'
    s = requests.get(url.format(zip_code,country_code)).json()
    p = requests.get(forc_url.format(zip_code,country_code)).json()
    loc_data = []
    loc_forc_data = []
   
    loc_weather = {
        'city' : city,
        'temperature': s['main']['temp'],
        'description': s['weather'][0]['description'],
        'icon': s['weather'][0]['icon'],
        'cloud': s['clouds']['all'],
        'windspeed': s['wind']['speed'],
    }
    for i in range(25):
        forc_weather = {
            'city' : city,
            'tem' : p['list'][i]['main']['temp'],
            'descript' : p['list'][i]['weather'][0]['description'],
            'date' : p['list'][i]['dt_txt'],
            'icon': p['list'][i]['weather'][0]['icon'],
            'cloudns' : p['list'][i]['clouds']['all'],
            'wind' : p['list'][i]['wind']['speed'],    
        }
        loc_forc_data.append(forc_weather)
    loc_data.append(loc_weather)
    context = {
        'loc_data' : loc_data,
        'loc_forc_data' : loc_forc_data,
        'city' : city
    }

    return render(request, 'weather_app/location.html', context)
