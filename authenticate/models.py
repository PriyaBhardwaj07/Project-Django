from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

gender_choices = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, address, gender, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have a valid email address")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            gender=gender,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, address, gender, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            gender=gender,
            password=password,
            **extra_fields
        )
        admin_role, _ = Role.objects.get_or_create(name='admin')
        user.role_id = admin_role
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50, null=False, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=100, null=False, unique=True)
    phone = models.CharField(max_length=15, default='N/A')
    address = models.CharField(max_length=200, default='default_address')
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')

    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'gender']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
