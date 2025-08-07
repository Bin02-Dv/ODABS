from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class DoctorProfile(models.Model):
    
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    speciallization = models.TextField(max_length=250, blank=True)
    biography = models.TextField(max_length=250, blank=True)
    profile_img = models.ImageField(upload_to='doctor/', blank=True)
    
    def __str__(self):
        return self.doctor.first_name, self.doctor.last_name

class DoctorAvailability(models.Model):
    
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    time_from = models.CharField(max_length=20, blank=True)
    time_to = models.CharField(max_length=10, blank=True)
    days = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.doctor.doctor.first_name, self.doctor.doctor.last_name

class PatientProfile(models.Model):
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, max_length=200)
    phone_number = models.CharField(blank=True, max_length=20)
    profile_img = models.ImageField(upload_to='patient/', blank=True)
    
    def __str__(self):
        return self.patient.first_name, self.patient.last_name

class Appointments(models.Model):
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    date = models.CharField(max_length=20, blank=True)
    time = models.CharField(max_length=10, blank=True)
    message_or_reason = models.TextField(max_length=250, blank=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    status = models.CharField(default='Pending')
    
    def __str__(self):
        return self.patient.patient.first_name, self.patient.patient.last_name

class MedicalHistory(models.Model):
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE)
    diagnosis = models.TextField(max_length=200, blank=True)
    prescription = models.TextField(max_length=200, blank=True)
    note = models.TextField(max_length=200, blank=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Prescription and note wrote by {self.doctor.doctor.first_name} for {self.patient.patient.first_name}"

