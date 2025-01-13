from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from prescriptions.models import Prescription
from appointments.models import Appointment


# @login_required
def add_prescription(request, appointment_id):
    # Ensure the appointment exists
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Ensure checkboxes are stored as True or False
        admission_required = 'admission_required' in request.POST
        revisit_required = 'revisit_required' in request.POST

        prescription_amount = request.POST.get('prescription_amount')

        Prescription.objects.create(
            appointment=appointment,
            doctor=appointment.doctor,
            patient=appointment.patient,
            admission_required=admission_required,
            revisit_required=revisit_required,
            lab_tests=request.POST.get('lab_tests', ""),
            medication_details=request.POST.get('medication_details', ""),
            dosage_instructions=request.POST.get('dosage_instructions', ""),
            prescription_amount=prescription_amount,
        )

        return redirect('appointments:doctor_appointments')

    return render(request, 'add_prescription.html', {'appointment': appointment})

# @login_required
def doctor_prescriptions(request):
    doctor = request.user.doctor
    prescriptions = Prescription.objects.filter(doctor=doctor)

    return render(request, 'doctor_prescriptions.html', {'prescriptions': prescriptions})

# @login_required
def patient_prescriptions(request):
    patient = request.user.patient_profile
    prescriptions = Prescription.objects.filter(patient=patient)

    return render(request, 'patient_prescriptions.html', {'prescriptions': prescriptions})
