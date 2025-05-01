from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_staff=False, is_active=True, **extra_fields):
        user = self.model(is_active=is_active, is_staff=is_staff, **extra_fields)
        if username:
            user.username = username
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(username, password, is_staff=True, is_superuser=True, **extra_fields)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
           
class Role(BaseModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=355, allow_unicode=True, null=True, blank=True)

    def __str__(self):
        return self.name
        
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    firstname = models.CharField(max_length=100, help_text="First name")
    lastname = models.CharField(max_length=100, help_text="Last name")
    username = models.CharField(max_length=60, unique=True)
    access_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField("status", default=True)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)

    is_active = models.BooleanField("active status", default=True)
    is_staff = models.BooleanField("is_staff", default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_permissions')


    def __str__(self):
        return self.firstname or self.lastname or self.username or "User None"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = 'users'
        ordering = ['-id']
