from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, "index.html")

def dash(request):
    return render(request, "patient/p-dash.html")

def d_dash(request):
    return render(request, "doctor/d-dash.html")

def a_dash(request):
    return render(request, "admin/a-dash.html")

def patient_signUp(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    "message": "Sorry Email already exist!!",
                    "status": False
                }
            )
        
        elif confirm_password != password:
            return JsonResponse(
                {
                    "message": "Sorry your password and confirm password is missed match!!",
                    "status": False
                }
            )
        
        else:
            new_user = User.objects.create_user(first_name=full_name, email=email, password=password)
            return JsonResponse(
                {
                    "message": "Patient Registered successfully...",
                    "status": True
                }
            )
    return JsonResponse(
        {
            "message": "No request was sent!!",
            "status": False
        }
    )
