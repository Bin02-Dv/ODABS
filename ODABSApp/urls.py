from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    # patient dashboard
    path('dash/', views.dash, name="dash"),
    
    # doctor dashboard
    path('d-dash/', views.d_dash, name="d-dash"),
    
    # admin dashboard
    path('a-dash/', views.a_dash, name="a-dash")
]
