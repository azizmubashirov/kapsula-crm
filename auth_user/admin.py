from django.contrib import admin
from .models import User

# Register your models here.
class Member(admin.ModelAdmin):
    list_display = (
        "firstname",
        "username",
        "is_staff",
    )


admin.site.register(User, Member)
