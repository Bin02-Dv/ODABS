from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    
    # patient dashboard
    path('dash/', views.dash, name="dash"),
    path('patient-signUp/', views.patient_signUp, name="patient-signUp"),
    path('p-profile/', views.p_profile, name="p-profile"),
    path('book-appointment/', views.book_appointment, name="book-appointment"),
    path('patient-appointments/', views.patient_appointments, name="patient-appointments"),
    path('medical-history/', views.medical_history, name="medical-history"),
    
    # doctor dashboard
    path('d-dash/', views.d_dash, name="d-dash"),
    path('doctor-signUp/', views.doctor_signUp, name="doctor-signUp"),
    path('d-profile/', views.d_profile, name="d-profile"),
    path('doctor-appointment-management/', views.doctor_appointment_management, name="doctor-appointment-management"),
    path('search-appointments/', views.search_appointments, name='search-appointments'),
    path('patient-record/', views.patient_record, name='patient-record'),
    
    # admin dashboard
    path('a-dash/', views.a_dash, name="a-dash"),
    path('all-appointments/', views.all_appointments, name='all-appointments'),
    path('all-users/', views.all_users, name="all-users"),
    path('delete-user/<int:id>/', views.delete_user, name="delete-user")
]
