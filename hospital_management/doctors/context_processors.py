from doctors.models import Department


def menu_links(request):
    d=Department.objects.all()
    return {'links':d}

