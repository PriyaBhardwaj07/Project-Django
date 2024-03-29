
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

gender_choices=(
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    
)

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    
    def create_user(self, email, first_name, last_name, phone, address, gender, password=None, password2=None):
        if not email:
            raise ValueError("User must have a valid email address 
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            address = address,
            gender = gender
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name,last_name, phone, address, gender, password=None):
        
        user=self.create_user(
            email = email,
            first_name =first_name,
            last_name = last_name,
            phone = phone,
            address = address,
            gender = gender,
            password = password
        )
        user.role_id = Role.objects.get(name='admin')
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=False, unique=True)
    phone = models.CharField(max_length= 15)
    address = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=gender_choices)
    registered_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    role_id = models.ForeignKey(Role,on_delete=models.SET_NULL, blank=True, null=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'gender'] #['First_Name','Password']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
      
        return True
    
    def has_module_perms(self, app_label):
        "Does user have permissions to view the app 'app_label'?"
        return True
    
    @property
    def is_active(self):
       
        return True
    
    @property
    def is_admin(self):
        return self.role_id.name == 'admin' if self.role_id else False
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        
        return self.is_admin
    
    


