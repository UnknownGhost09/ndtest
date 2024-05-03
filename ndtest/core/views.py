from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request,'dashboard.html')


def total_devices(request):
    return render(request,'total_devices.html')

def alerts(request):
    return render(request,'alerts.html')

def tickets(request):
    return render(request,'tickets.html')