from django.urls import path
from .views import calculate_distance_view,hello


urlpatterns = [
    path('',calculate_distance_view,name='distance'),
    path('hello/',hello,name='hello'),
]
