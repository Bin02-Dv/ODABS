from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, DoctorAvailability, PatientProfile, Appointments, MedicalHistory

# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required(login_url='/')
def dash(request):
    current_user = User.objects.get(username=request.user)
    current_patient = PatientProfile.objects.filter(patient=current_user).first()
    return render(request, "patient/p-dash.html", {'current_user': current_user, 'current_patient': current_patient})

@login_required(login_url='/')
def d_dash(request):
    current_doctor = DoctorProfile.objects.get(doctor=request.user)
    availabililty = DoctorAvailability.objects.filter(doctor=current_doctor).first()
    if request.method == 'POST':
        
        time_from = request.POST.get("from", "")
        time_to = request.POST.get("to", "")
        days = request.POST.get("days", "")
        
        if not availabililty:
            
            DoctorAvailability.objects.create(
                doctor=current_doctor, time_from=time_from, time_to=time_to, days=days
            )
        
        else:
            availabililty.time_from = time_from
            availabililty.time_to = time_to
            availabililty.days = days
            
            availabililty.save()
            
        return JsonResponse({
            "message": "Availability Updated successfully...",
            "success": True
        })    
    return render(request, "doctor/d-dash.html", {'availability': availabililty})

@login_required(login_url='/')
def search_appointments(request):
    doctor = DoctorProfile.objects.get(doctor=request.user)
    appointments = Appointments.objects.filter(doctor=doctor).order_by('-date', '-time')

    date = request.GET.get('date')
    status = request.GET.get('status')

    if date:
        appointments = appointments.filter(date=date)
    if status:
        appointments = appointments.filter(status=status)

    return render(request, 'doctor/search-appointments.html', {
        'appointments': appointments,
    })

@login_required(login_url='/')
def patient_record(request):
    current_doctor = DoctorProfile.objects.get(doctor=request.user)
    records = MedicalHistory.objects.filter(doctor=current_doctor)
    context = {
        'records': records
    }
    return render(request, 'doctor/patient-record.html', context)

@login_required(login_url='/')
def doctor_appointment_management(request):
    current_doctor = DoctorProfile.objects.get(doctor=request.user)
    appointments = Appointments.objects.filter(doctor=current_doctor).order_by('-date')
    
    if request.method == 'POST':
        note = request.POST.get('note', '')
        diagonosis = request.POST.get('diagonosis', '')
        prescription = request.POST.get('prescription', '')
        status = request.POST.get('status', '')
        patient = request.POST.get('patient', '')
        appointment = request.POST.get('appointment', '')
        
        appointment_existent_check = MedicalHistory.objects.filter(appointment=appointment).first()
        try:
            get_appointment = Appointments.objects.get(id=appointment)
        except Appointments.DoesNotExist:
            return JsonResponse({
                "message": "Sorry we couldn't find this appointment!!",
                "success": False
            })
        try:
            get_patient = PatientProfile.objects.get(id=patient)
        except Appointments.DoesNotExist:
            return JsonResponse({
                "message": "Sorry we couldn't find this appointment!!",
                "success": False
            })
        
        if not note or not diagonosis or not prescription:
            return JsonResponse({
                "message": "Sorry to complete the task.. Note, Diagonosis and Prescription are required!!",
                "success": False
            })
        
        elif appointment_existent_check:
            appointment_existent_check.note = note
            appointment_existent_check.diagnosis = diagonosis
            appointment_existent_check.prescription = prescription
            get_appointment.status = status
            
            appointment_existent_check.save()
            get_appointment.save()
            
            return JsonResponse({
                "message": "Appointment Updated Successfully...",
                "success": True
            })
        else:
            MedicalHistory.objects.create(
                patient=get_patient, doctor=current_doctor, appointment=get_appointment, diagnosis=diagonosis,
                prescription=prescription, note=note
            )
            get_appointment.status = status
            get_appointment.save()
            return JsonResponse({
                "message": "Appointment Updated Successfully...",
                "success": True
            })
    context = {
        'appointments': appointments
    }
    return render(request, 'doctor/manage-appointments.html', context)

@login_required(login_url='/')
def patient_appointments(request):
    current_user = PatientProfile.objects.get(patient=request.user)
    apppointments = Appointments.objects.filter(patient=current_user)
    context = {
        'appointments': apppointments
    }
    return render(request, "patient/my-appointment.html", context)

@login_required(login_url='/')
def d_profile(request):
    current_user = request.user
    current_doctor = DoctorProfile.objects.filter(doctor=current_user).first()

    if request.method == 'POST':
        specialization = request.POST.get('specialization', '')
        bio = request.POST.get('bio', '')
        photo = request.FILES.get('photo', None)

        clean_sp = specialization.replace(",", " | ")

        if not current_doctor:
            DoctorProfile.objects.create(
                doctor=current_user,
                speciallization=clean_sp,
                biography=bio,
                profile_img=photo
            )
        else:
            current_doctor.speciallization = clean_sp
            current_doctor.biography = bio
            if photo:
                current_doctor.profile_img = photo
            current_doctor.save()

        return JsonResponse({
            "message": "Profile Updated successfully...",
            "success": True
        })

    return render(request, "doctor/profile.html", {
        'current_user': current_user,
        'current_doctor': current_doctor
    })

@login_required(login_url='/')
def p_profile(request):
    current_user = User.objects.get(username=request.user)
    current_patient = PatientProfile.objects.filter(patient=current_user).first()
    if request.method == 'POST':
        email = request.POST.get("email", "")
        phone_number = request.POST.get("phone_number", "")
        photo = request.FILES.get("photo", None)
        
        if not current_patient:
            
            PatientProfile.objects.create(
                patient=current_user, email=email, phone_number=phone_number,
                profile_img=photo
            )
        
        else:
            current_patient.email = email
            current_patient.phone_number = phone_number
            
            if photo:
                current_patient.profile_img = photo
            current_patient.save()
        return JsonResponse({
            "message": "Profile Updated successfully...",
            "success": True
        })
    return render(request, 'patient/profile.html', {'current_patient': current_patient, 'current_user': current_user})

@login_required(login_url='/')
def book_appointment(request):
    doctors = DoctorAvailability.objects.all()
    currrent_patient = PatientProfile.objects.get(patient=request.user)
    if request.method == 'POST':
        doc_id = request.POST.get("doctor", "")
        date = request.POST.get("date", "")
        time = request.POST.get("time", "")
        message_or_reason = request.POST.get("message", "")
        
        try:
        
            doctor = DoctorProfile.objects.get(id=doc_id)
            Appointments.objects.create(
                patient=currrent_patient,
                doctor=doctor, date=date, time=time, message_or_reason=message_or_reason
            )
            
            return JsonResponse({
                "message": "Appointment Booked successfully...",
                "success": True
            })
                
        except DoctorProfile.DoesNotExist:
            return JsonResponse({
                    "message": "We Couldn't find the selected doctor!!",
                    "success": False
                })
    context = {
        "doctors": doctors
    }
    return render(request, "patient/book-appointment.html", context)

@login_required(login_url='/')
def medical_history(request):
    currrent_patient = PatientProfile.objects.get(patient=request.user)
    m_history = MedicalHistory.objects.filter(patient=currrent_patient).order_by('-date')
    context = {
        'm_history': m_history
    }
    return render(request, 'patient/medical-history.html', context)

@login_required(login_url='/')
def a_dash(request):
    doctors = DoctorProfile.objects.all().count()
    patients = PatientProfile.objects.all().count()
    appointment = Appointments.objects.all().count()
    
    context = {
        'doctors': doctors,
        'patients': patients,
        'appointment': appointment
    }
    return render(request, "admin/a-dash.html", context)

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

@login_required(login_url='/')
def all_appointments(request):
    apppointments = Appointments.objects.all().order_by('-id')
    doctors = DoctorProfile.objects.all().count()
    patients = PatientProfile.objects.all().count()
    appointment = Appointments.objects.all().count()
    context = {
        'appointment': appointment,
        'appointments': apppointments,
        'doctors': doctors,
        'patients': patients,
    }
    return render(request, 'admin/all-appointments.html', context)

@login_required(login_url='/')
def all_users(request):
    users = User.objects.all().order_by('-id')
    doctors = DoctorProfile.objects.all().count()
    patients = PatientProfile.objects.all().count()
    appointment = Appointments.objects.all().count()
    context = {
        'users': users,
        'appointment': appointment,
        'doctors': doctors,
        'patients': patients
    }
    
    return render(request, 'admin/all_users.html', context)


@login_required(login_url='/')
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('/all-users')