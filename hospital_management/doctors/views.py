from django.shortcuts import render, redirect
from doctors.models import Department,Doctor
from django.db.models import Q
from django.contrib.auth.hashers import make_password

def alldepartments(request):
    d=Department.objects.all()

    return render(request, 'department.html',{'dep':d})

def alldoctors(request,d):
    d = Department.objects.get(id=d)
    doc = Doctor.objects.filter(department=d)
    return render(request,'doctor.html',{'dep':d,'doctor':doc})

def doctorsdetails(request,d):
    doc=Doctor.objects.get(id=d)
    return render(request,'doctordetail.html',{'doctor':doc})

def service(request):
    return render(request,'service.html')

def add_department(request):
    if request.method=='POST':
        name= request.POST['n']
        desc=request.POST['d']
        image=request.FILES['i']

        k=Department.objects.create(name=name,description=desc,image=image)
        k.save()
        return redirect('doctors:department')
    return render(request,'add_department.html')

def add_doctor(request):
    if request.method=='POST':
        name= request.POST['n']
        firstname = request.POST['f']
        lastname = request.POST['l']
        desc=request.POST['d']
        # password = request.POST['pw']
        image=request.FILES.get('i')
        email=request.POST['e']
        phone=request.POST['p']
        specialization = request.POST['s']
        department = request.POST['d']

        # Hash the password for security
        # hashed_password = make_password(password)

        d=Department.objects.get(name=department)
        doc=Doctor.objects.create(name=name,first_name=firstname,last_name=lastname,description=desc,image=image,email=email,phone_number=phone,specialization=specialization,department=d) #password=hashed_password
        doc.save()

        return redirect('doctors:department')
    return render(request, 'add_doctor.html')

def search_doctor(request):
    query=""
    d=None
    if request.method=="POST":
        query=request.POST['q']
        if query:
            d=Doctor.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(specialization__icontains=query))

    return render(request,'doctor_search.html',{'doctor':d,'q':query})
