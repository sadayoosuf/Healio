from django.shortcuts import render, redirect , get_object_or_404
from appointments.models import Appointment
from doctors.models import Doctor, Department
# from django.contrib.auth.decorators import login_required

def book_appointment(request):

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
            patient = request.user.patient_profile
        except AttributeError:
            # Handle the case where the user is not a patient
            patient = None

        if patient:
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

            return redirect('appointments:appointment_history')


    full_name = f"{request.user.first_name} {request.user.last_name}"
    return render(request, 'appointment.html', {'full_name': full_name, 'doctors': doctors})

# @login_required
def appointment_history(request):
    try:
        # Access the patient's profile using the related_name
        patient = request.user.patient_profile
        appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
    except AttributeError:
        # Handle the case where the user is not a patient
        appointments = []

    return render(request, 'appointment_history.html', {'appointments': appointments})


def doctor_appointments(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor).order_by('-date', '-time')

    if request.method == 'POST':
        # Update appointment status (Confirmed or Cancelled)
        appointment_id = request.POST.get('appointment_id')
        new_status = request.POST.get('status')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = new_status
        appointment.save()
        return redirect('appointments:doctor_appointments')

    return render(request, 'doctor_appointments.html', {'appointments': appointments})

# Edit Appointment View
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        department_name = request.POST['d']
        doctor_name = request.POST['doc']
        date = request.POST['date']
        time = request.POST['time']
        phone = request.POST['phone']
        message = request.POST['message']

        selected_department = Department.objects.get(name=department_name)
        doc = Doctor.objects.get(id=doctor_name)

        appointment.department = selected_department
        appointment.doctor = doc
        appointment.date = date
        appointment.time = time
        appointment.phone_number = phone
        appointment.message = message
        appointment.save()

        return redirect('appointments:appointment_history')

    return render(request, 'edit_appointment.html', {
        'appointment': appointment,
        'doctors': doctors
    })

#delete appointment
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments:appointment_history')

    return render(request, 'delete_appointment.html', {'appointment': appointment})