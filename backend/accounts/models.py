from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from simple_history.models import HistoricalRecords

class UserAccountManager(BaseUserManager):

    def create_user(self, email, name, password, user_type=None):
        if email is None:
            raise TypeError('Email address is mandatory')
        if name is None:
            raise TypeError('Name is mandatory')
        if password is None:
            raise TypeError('Password is mandatory')
        if user_type is None:
            user_type = "USER"
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          user_type=user_type)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, user_type=None):
        user = self.create_user(
            email, name, password, "ADMIN")
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):

    # user types
    UserType = [
        ('USER', 'USER'),
        ('DELIVERY', 'DELIVERY'),
        ('ADMIN', 'ADMIN')
    ]

    # required fields
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    # other fields
    phone = models.CharField(max_length=10, blank=True)
    user_type = models.CharField(
        max_length=50, choices=UserType, default='USER')
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=4, blank=True)

    history = HistoricalRecords()
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_user_type(self):
        return self.user_type

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = ' User Accounts'
