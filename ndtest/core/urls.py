from django.contrib import admin
from django.urls import path,include
from  .views import *  

urlpatterns = [
    path('',dashboard),
    path('total_devices',total_devices),
    path('alerts',alerts),
    path('ticket',tickets)

    
]