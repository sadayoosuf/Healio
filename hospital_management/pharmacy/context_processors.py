from pharmacy.models import Category,Cart


def menu_category_links(request):
    c=Category.objects.all()
    return {'links1':c}

def count_items(request):
    u=request.user
    count=0
    if request.user.is_authenticated:
        try:
            c=Cart.objects.filter(user=u)
            for i in c:
                count+=i.quantity
        except:
            count=0
    return {'c':count}

