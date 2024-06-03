from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# creating a custom user
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):  # the **extra_fields is to allow additional field to be added dynamically to the create_user function
        if not email:
            raise ValueError(_("The email must be set"))
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    
    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("The superuser must be is_staff"))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must be is_superuser"))
        
        return self.create_user(email, password, **extra_fields)
    
    
