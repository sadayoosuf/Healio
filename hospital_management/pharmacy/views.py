from django.shortcuts import render,redirect,get_object_or_404
from pharmacy.models import Category,Medicine,Cart,OrderDetails,Payment
from django.views.decorators.csrf import csrf_exempt
import razorpay
from users.models import CustomUser
from django.contrib.auth import login
from django.db.models import Q


def allcategories(request):
    c = Category.objects.all()
    return render(request, 'pharmacy_category.html', {'cat': c})

def allmedicines(request,m):
    c=Category.objects.get(id=m)
    m=Medicine.objects.filter(category=c)
    return render(request, 'pharmacy_medicine.html', {'cat': c, 'medicine': m})

def medicinesdetails(request,m):
    m=Medicine.objects.get(id=m)
    return render(request,'pharmacy_medicinedetail.html',{ 'medicine': m})

def addcategory(request):
    if request.method=='POST':
        name= request.POST['n']
        desc=request.POST['d']
        image=request.FILES['i']

        k=Category.objects.create(name=name,description=desc,image=image)
        k.save()
        return redirect('pharmacy:category')
    return render(request,'pharmacy_addcategory.html')

def addmedicine(request):
    if request.method == 'POST':
        name = request.POST['n']
        description = request.POST['d']
        image = request.FILES.get('i')
        price = request.POST['p']
        stock = request.POST['s']
        expiry_date = request.POST['e']
        manufacturer = request.POST['m']
        category_name = request.POST['c']  # Read category name from the form field

        # Get the Category object matching the category name
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return render(request, 'pharmacy_addmedicine.html', {'error': 'Category does not exist'})

        # Create a new Medicine object
        medicine = Medicine.objects.create(
            name=name,
            description=description,
            image=image,
            price=price,
            stock=stock,
            expiry_date=expiry_date,
            manufacturer=manufacturer,
            category=category
        )
        medicine.save()

        return redirect('pharmacy:category')  # Redirect after successful product addition

    return render(request, 'pharmacy_addmedicine.html')

def add_to_cart(request,i):
    m=Medicine.objects.get(id=i)
    u=request.user
    try:
        c = Cart.objects.get(user=u,medicine=m)
        if(m.stock>0):
            c.quantity+=1
            c.save()
            m.stock-=1
            m.save()

    except:
        c=Cart.objects.create(medicine=m,user=u,quantity=1)
        c.save()
        m.stock-=1
        m.save()

    return redirect('pharmacy:cartview')

# @login_required
def cart_view(request):
    u=request.user
    total=0
    c=Cart.objects.filter(user=u)
    for i in c:
        total+=i.quantity*i.medicine.price
    return render(request,'pharmacy_cart.html',{'cart':c,'total':total})


def cart_remove(request,i):
    m=Medicine.objects.get(id=i)
    u=request.user

    try:
        c=Cart.objects.get(user=u,medicine=m)
        if(c.quantity>1):
            c.quantity-=1
            c.save()
            m.stock+=1
            m.save()
        else:
            c.delete()
            m.stock += 1
            m.save()
    except:
        pass
    return redirect('pharmacy:cartview')

def cart_delete(request,i):
    m=Medicine.objects.get(id=i)
    u=request.user

    try:
        c=Cart.objects.get(user=u,medicine=m)
        c.delete()
        m.stock += c.quantity
        m.save()
    except:
        pass
    return redirect('pharmacy:cartview')

def order_form(request):
    if(request.method=="POST"):
        address=request.POST['a']
        phone=request.POST['p']
        pin=request.POST['pi']

        u=request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total+=i.quantity*i.medicine.price
        total=int(total*100)
        client=razorpay.Client(auth=('rzp_test_cQky6LUBsfvART','UOkwN4DKb9k2dZF8kDqedkA2')) #creates a client connection
        # using razorpay id and secret code

        response_payment=client.order.create(dict(amount=total,currency="INR"))  #creates an order with razorpay using razorpay client
        # print(response_payment)
        order_id=response_payment['id']  #Retrieves the order_id from response
        order_status=response_payment['status'] #retrive status from response
        if(order_status=="created"):  #if status is created then store order_id in payment and order_detail table
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=OrderDetails.objects.create(medicine=i.medicine,user=u,no_of_items=i.quantity,address=address,phone_no=phone,pin=pin,order_id=order_id)
                o.save()
        else:
            pass

        response_payment['name']=u.username #additional information name

        return render(request,'pharmacy_payment.html',{'payment':response_payment})



    return render(request,'pharmacy_orderform.html')

@csrf_exempt    #csrf verification failed-error
def payment_status(request,u):
    user = get_object_or_404(CustomUser, username=u)
    if(not request.user.is_authenticated):  #if user is not authenticated
        login(request,user) #allowing request user to login
    if(request.method=="POST"):
        response=request.POST

        print("Response:", response)
        print("Username:", u)

        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature'],
        }

        client = razorpay.Client(auth=('rzp_test_cQky6LUBsfvART', 'UOkwN4DKb9k2dZF8kDqedkA2'))
        print(client)
        try:
            status=client.utility.verify_payment_signature(param_dict) #to check the authenticity of the razorpay signature
            print(status)
            #to retrieve a particular record in payment table whole order id matches the response order is
            p=Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id=response['razorpay_payment_id'] #adds the payment id after successfull payment
            p.paid=True  #changes paid status to true
            p.save()

            # user=User.objects.get(username=u)
            o=OrderDetails.objects.filter(user=user,order_id=response['razorpay_order_id']) #retrieve the particular record in order_details
            #matching with current user and response order_id
            for i in o:
                i.payment_status="paid"
                i.save()

            #after successful payment deletes the item in cart for particular user
            c=Cart.objects.filter(user=user)
            c.delete()


        except:
            print("hello")




    return render(request,'pharmacy_paymentstatus.html',{'status':status})


def order_view(request):
    u=request.user
    o=OrderDetails.objects.filter(user=u)

    return render(request,'pharmacy_orderview.html',{'orders':o})


def add_stock(request,m):
    med=Medicine.objects.get(id=m)
    if(request.method=="POST"):
        med.stock=request.POST['n']
        med.save()
        return redirect('pharmacy:category')
    return render(request,'pharmacy_addstock.html',{'medicine':med})

def search_medicine(request):
    query=""
    m=None
    if request.method=="POST":
        query=request.POST['q']
        if query:
            m=Medicine.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query))

    return render(request,'pharmacy_search.html',{'medicine':m,'q':query})
