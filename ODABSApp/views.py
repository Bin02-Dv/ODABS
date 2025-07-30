from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def dash(request):
    return render(request, "patient/p-dash.html")

def d_dash(request):
    return render(request, "doctor/d-dash.html")

def a_dash(request):
    return render(request, "admin/a-dash.html")
