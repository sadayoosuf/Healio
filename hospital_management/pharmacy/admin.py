from django.contrib import admin

from pharmacy.models import Category,Medicine,Cart,OrderDetails,Payment


admin.site.register(Category)
admin.site.register(Medicine)
admin.site.register(Cart)
admin.site.register(OrderDetails)
admin.site.register(Payment)


