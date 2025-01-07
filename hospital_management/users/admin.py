from django.contrib import admin
from users.models import CustomUser

# Register the CustomUser model with the admin interface
admin.site.register(CustomUser)
