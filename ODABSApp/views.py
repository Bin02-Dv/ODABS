from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required(login_url='/')
def dash(request):
    return render(request, "patient/p-dash.html")

@login_required(login_url='/')
def d_dash(request):
    return render(request, "doctor/d-dash.html")

@login_required(login_url='/')
def a_dash(request):
    return render(request, "admin/a-dash.html")

def patient_signUp(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    "message": "Sorry Email already exist!!",
                    "success": False
                }
            )
        
        elif User.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    "message": "Sorry Username already exist!!",
                    "success": False
                }
            )
        
        elif confirm_password != password:
            return JsonResponse(
                {
                    "message": "Sorry your password and confirm password is missed match!!",
                    "success": False
                }
            )
        
        else:
            new_user = User.objects.create_user(first_name=full_name, email=email, last_name='patient', username=username, password=password)
            return JsonResponse(
                {
                    "message": "Your account has been Registered successfully...",
                    "success": True
                }
            )
    return JsonResponse(
        {
            "message": "No request was sent!!",
            "success": False
        }
    )


def doctor_signUp(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    "message": "Sorry Email already exist!!",
                    "success": False
                }
            )
        
        elif User.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    "message": "Sorry Username already exist!!",
                    "success": False
                }
            )
        
        elif confirm_password != password:
            return JsonResponse(
                {
                    "message": "Sorry your password and confirm password is missed match!!",
                    "success": False
                }
            )
        
        else:
            new_user = User.objects.create_user(first_name=full_name, email=email, last_name='doctor', username=username, password=password)
            return JsonResponse(
                {
                    "message": "Your account has been Registered successfully...",
                    "success": True
                }
            )
    return JsonResponse(
        {
            "message": "No request was sent!!",
            "success": False
        }
    )

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        url = ''
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_superuser:
                url = '/a-dash/'
            elif user.last_name == 'doctor':
                url = '/d-dash/'
            else:
                url = '/dash/'
            auth.login(request, user)
            return JsonResponse(
                {
                    "message": "Login successfully...",
                    "success": True,
                    "url": url
                }
            )
        else:
            return JsonResponse(
                {
                    "message": "Invalid Username or password",
                    "success": False
                }
            )
    return JsonResponse(
        {
            "message": "No request sent!!",
            "success": False
        }
    )

def logout(request):
    auth.logout(request)
    return redirect('/')
