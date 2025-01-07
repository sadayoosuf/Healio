from django.shortcuts import render, redirect
from appointments.models import Appointment
from doctors.models import Doctor, Department
# from django.contrib.auth.decorators import login_required

def book_appointment(request):
    # Fetch all doctors
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        department_name = request.POST['d']
        doctor_name = request.POST['doc']
        date = request.POST['date']
        time = request.POST['time']
        name = request.POST['name']
        phone = request.POST['phone']
        message = request.POST['message']

        selected_department = Department.objects.get(name=department_name)
        doc = Doctor.objects.get(id=doctor_name)

        try:
            # Access the patient's profile using the related_name 'patient_profile'
            patient = request.user.patient_profile  # Correctly accessing the Patient profile
        except AttributeError:
            # Handle the case where the user is not a patient
            patient = None  # You can handle this scenario as needed (e.g., showing an error message)

        if patient:
            # Create the appointment only if the user has a patient profile
            a = Appointment.objects.create(
                patient=patient,
                date=date,
                time=time,
                phone_number=phone,
                message=message,
                department=selected_department,
                doctor=doc
            )
            a.save()

            return redirect('appointments:appointment_history')  # Redirect after saving

    # Provide the user's full name for pre-filling
    full_name = f"{request.user.first_name} {request.user.last_name}"
    return render(request, 'appointment.html', {'full_name': full_name, 'doctors': doctors})

# @login_required
def appointment_history(request):
    try:
        # Access the patient's profile using the related_name
        patient = request.user.patient_profile
        # Fetch the appointments for the logged-in patient
        appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
    except AttributeError:
        # Handle the case where the user is not a patient
        appointments = []

    return render(request, 'appointment_history.html', {'appointments': appointments})


def doctor_appointments(request):
    # Fetch appointments for the logged-in doctor
    appointments = Appointment.objects.filter(doctor=request.user.doctor).order_by('-date', '-time')

    if request.method == 'POST':
        # Update appointment status (Confirmed or Cancelled)
        appointment_id = request.POST.get('appointment_id')
        new_status = request.POST.get('status')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = new_status
        appointment.save()
        return redirect('appointments:doctor_appointments')  # Redirect to refresh the page

    return render(request, 'doctor_appointments.html', {'appointments': appointments})
