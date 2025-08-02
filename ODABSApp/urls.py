from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    
    # patient dashboard
    path('dash/', views.dash, name="dash"),
    path('patient-signUp/', views.patient_signUp, name="patient-signUp"),
    
    # doctor dashboard
    path('d-dash/', views.d_dash, name="d-dash"),
    path('doctor-signUp/', views.doctor_signUp, name="doctor-signUp"),
    
    # admin dashboard
    path('a-dash/', views.a_dash, name="a-dash")
]
