from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from geopy.distance import geodesic
import folium
from .models import Measurement
from .forms import DistanceForm
from geopy.geocoders import Nominatim
from .utils import get_geo,get_zoom,get_center_coordinates,get_ip_address


def calculate_distance_view(request):
    distance = None
    destination = None
    obj = get_object_or_404(Measurement, id=1)
    form = DistanceForm(request.POST or None)
    geolocation = Nominatim(user_agent='distance')

    ip = '72.14.207.99'
    country, city, lat, lon = get_geo(ip)
    location = geolocation.geocode(city)
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)
#   initial folium map
    m = folium.Map(width= 800, height = 600, location=get_center_coordinates(l_lat, l_lon), zoom_start= 8)
#   location marker
    folium.Marker([lat,lon],tooltip="click here to see more",popup=city['city'],
                  icon=folium.Icon(color='purple')).add_to(m)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)

            destination_ = form.cleaned_data.get('destination')
            destination = geolocation.geocode(destination_)
            d_lat = destination.latitude
            d_long = destination.longitude
            pointB = (d_lat, d_long)

            distance = round(geodesic(pointA, pointB).km, 2)
#           initial folium
            m = folium.Map(width=800, height=600, location = get_center_coordinates(l_lat, l_lon), zoom_start=get_zoom(distance))
#           location marker
            folium.Marker([l_lat,l_lon], tooltip="click here to see more", popup=city['city'],
                          icon=folium.Icon(color='purple')).add_to(m)
#           destination marker
            folium.Marker([d_lat,d_long],popup=destination,tooltip="the destination",
                          icon=folium.Icon(color='red')).add_to(m)
#           add line
            line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
            m.add_child(line)

            instance.location = location
            instance.distance = distance
            instance.save()
    m = m._repr_html_()

    context = {
        'destination':destination,
        'distance': distance,
        'form': form,
        'map':m,
    }

    return render(request, 'distance/geo.html', context)


def hello(request):
    return HttpResponse('hello world')
