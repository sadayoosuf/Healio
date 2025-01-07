from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from doctors.models import Doctor,Department
from patients.models import Patient
from users.models import CustomUser

# Admin Registration
def admin_register(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        a = request.POST['a']
        n = request.POST['n']

        if p == cp:
            user = CustomUser.objects.create_user(username=u, password=p, first_name=f, last_name=l, email=e, address=a, phone=n, is_admin=True)
            user.save()
            return redirect('users:login')
        else:
            return HttpResponse("Passwords are not matching")

    return render(request, 'admin_register.html')

# doctor registration
def doctor_register(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        n = request.POST['n']
        specialization = request.POST['specialization']
        department_id = request.POST['department']
        description = request.POST.get('description', '')
        image = request.FILES.get('image', None)  # Get the image file if provided

        if p == cp:
            user = CustomUser.objects.create_user(username=u, password=p, first_name=f, last_name=l, email=e, phone=n, is_doctor=True)
            user.save()

            department = Department.objects.get(id=department_id)  # Get the selected department

            doctor = Doctor.objects.create(
                user=user,
                name=f"{f} {l}",
                first_name=f,
                last_name=l,
                email=e,
                phone_number=n,
                specialization=specialization,
                department=department,
                description=description,
                image=image
            )
            doctor.save()

            return redirect('users:login')
        else:
            return HttpResponse("Passwords are not matching")

    # Pass departments to the context to populate the department dropdown
    departments = Department.objects.all()
    return render(request, 'doctor_register.html', {'departments': departments})
# Patient Registration
def patient_register(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        a = request.POST['a']
        n = request.POST['n']
        dob = request.POST['dob']
        gender = request.POST['gender']
        primary_doctor_id = request.POST.get('primary_doctor')  # Optional field

        if p == cp:
            # Create the CustomUser instance
            user = CustomUser.objects.create_user(
                username=u,
                password=p,
                first_name=f,
                last_name=l,
                email=e,
                address=a,
                phone=n,
                is_patient=True
            )
            user.save()

            # Get the selected primary doctor (if any)
            primary_doctor = None
            if primary_doctor_id:
                try:
                    primary_doctor = Doctor.objects.get(id=primary_doctor_id)
                except Doctor.DoesNotExist:
                    primary_doctor = None

            # Create the Patient instance
            patient = Patient.objects.create(
                user=user,
                name=f"{f} {l}",
                first_name=f,
                last_name=l,
                phone_number=n,
                date_of_birth=dob,
                gender=gender,
                primary_doctor=primary_doctor
            )
            patient.save()

            return redirect('users:login')
        else:
            return HttpResponse("Passwords are not matching")

    # Fetch all doctors for the dropdown in the template
    doctors = Doctor.objects.all()
    return render(request, 'patient_register.html', {'doctors': doctors})


# User Login
def user_login(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u, password=p)

        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('doctors:department')  # Redirect to the Admin dashboard
            elif user.is_doctor:
                return redirect('doctors:department')  # Redirect to the Doctor dashboard
            elif user.is_patient:
                return redirect('doctors:department')  # Redirect to the Patient dashboard
            else:
                return HttpResponse("Invalid user type.")
        else:
            return HttpResponse("Invalid username or password")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('users:login')

