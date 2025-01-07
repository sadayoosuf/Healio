from django.db import models
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescription_date = models.DateField(auto_now_add=True)
    prescription_amount=models.IntegerField(blank=True, null=True)
    admission_required = models.BooleanField(default=False)
    revisit_required = models.BooleanField(default=False)
    lab_tests = models.TextField(blank=True, null=True)  # List of lab tests, if any

    # Medication details
    medication_details = models.TextField(help_text="Details of medications prescribed.")
    dosage_instructions = models.TextField(help_text="Dosage details (e.g., before food, after food, AM/PM).")

    def __str__(self):
        return f"Prescription for {self.patient.first_name} {self.patient.last_name} by Dr. {self.doctor.first_name} {self.doctor.last_name}"

