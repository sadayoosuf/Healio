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

        # Create the prescription
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

        # Redirect back to the appointments list after saving the prescription
        return redirect('appointments:doctor_appointments')

    return render(request, 'add_prescription.html', {'appointment': appointment})

# @login_required
def doctor_prescriptions(request):
    # Fetch all prescriptions for the logged-in doctor
    doctor = request.user.doctor  # Assuming the user is linked to a doctor instance
    prescriptions = Prescription.objects.filter(doctor=doctor)

    # Pass prescriptions to the template
    return render(request, 'doctor_prescriptions.html', {'prescriptions': prescriptions})

# @login_required
def patient_prescriptions(request):
    # Get the currently logged-in patient
    patient = request.user.patient_profile  # Assuming the user has a related patient profile

    # Get all prescriptions for this patient
    prescriptions = Prescription.objects.filter(patient=patient)

    return render(request, 'patient_prescriptions.html', {'prescriptions': prescriptions})
