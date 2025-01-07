from django.db import models
from users.models import CustomUser  # Import CustomUser instead of default User


# Medicine Category
class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="category")

    def __str__(self):
        return self.name


# Medicine Model
class Medicine(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="category", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    expiry_date = models.DateField()
    manufacturer = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)  # One-time creation timestamp
    updated = models.DateTimeField(auto_now=True)  # Updated every time the record changes
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # def is_in_stock(self):
    #     return self.stock > 0

    def is_expired(self):
        from django.utils.timezone import now
        return self.expiry_date < now().date()


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="carts")  # Patient as user
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.medicine.price * self.quantity

    def __str__(self):
        return f"Cart({self.user.username} - {self.medicine.name})"


# Order Details Model
class OrderDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")  # Patient as user
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="orders")
    no_of_items = models.IntegerField()
    address = models.TextField()
    phone_no = models.BigIntegerField()
    pin = models.IntegerField()

    order_id = models.CharField(max_length=100, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    payment_status = models.CharField(max_length=20, default="pending")
    delivery_status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Order({self.order_id} - {self.user.username})"


# Payment Model
class Payment(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=50, blank=True)
    razorpay_payment_id = models.CharField(max_length=50, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment({self.name} - {self.order_id})"
