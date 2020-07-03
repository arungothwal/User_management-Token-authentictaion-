from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import ugettext_lazy as _
from rest_framework_jwt.utils import jwt_payload_handler
from django.contrib.auth.models import PermissionsMixin
import jwt
from django.conf import settings
from django.contrib.sessions.models import Session



class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class MyUser(AbstractBaseUser,PermissionsMixin):


    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField( max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),

    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True,null=True)

    is_staff = models.BooleanField( default=False)
    is_active = models.BooleanField(default=True)
    Address=models.CharField(max_length=30,blank=True)
    dob=models.DateField(max_length=10,blank=True,null=True)


    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_jwt(self):
        """Function for creating JWT for Authentication Purpose"""
        payload = jwt_payload_handler(self)
        token = jwt.encode(payload, settings.SECRET_KEY)
        auth_token = token.decode('unicode_escape')
        return auth_token

    def remove_all_sessions(self):
        user_sessions = []
        all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in Session.objects.all():
            if str(self.pk) == session.get_decoded().get('_auth_user_id'):
                user_sessions.append(session.pk)
        return Session.objects.filter(pk__in=user_sessions).delete()

    def __str__(self):
        return self.email


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')




