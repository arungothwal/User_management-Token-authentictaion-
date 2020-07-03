# # from django.core.mail import send_mail
# # from django.conf import settings
# # from rest_framework.response import Response
# #
# #
# # def email(request):
# #     subject = 'Thank you for registering to our site'
# #     message = ' it  means a world to us '
# #     email_from = settings.EMAIL_HOST_USER
# #     recipient_list = ['receiver@gmail.com',]
# #     send_mail( subject, message, email_from, recipient_list )
# #     return Response('redirect to a new page')
# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext as _
import re
from rest_framework import status
from .serializers import MyUserSerializer
from rest_framework.response import Response

from django.core.exceptions import ValidationError


"""
    Validate whether the password contains minimum one uppercase, one digit and one symbol.
"""
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) <= 8:
        val = False
        raise ValidationError('length should be not be greater than 8')

    if not any(char.isdigit() for char in passwd):
        val = False
        raise ValidationError('Password should have at least one numeral')

    if not any(char.isupper() for char in passwd):
        val = False
        raise ValidationError('Password should have at least one uppercase letter')

    if not any(char.islower() for char in passwd):
        val = False
        raise ValidationError('Password should have at least one lowercase letter')

    if not any(char in SpecialSym for char in passwd):
        val = False
        raise ValidationError('Password should have at least one of the symbols $@#')
    if val:
        return passwd
