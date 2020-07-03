from django.conf.urls import url
from django.urls import path,include


from .views import *
from . import views

urlpatterns = [
    url(r'^signup', CreateUser.as_view()),
    url(r'^login', Login.as_view()),
    url(r'^logout', Logout.as_view()),
    url(r'^getuser', Get_all_user.as_view()),
    url(r'^change_password', Change_password.as_view()),
    # path("<phone>/", get_phone_number.as_view(), name="OTP Gen"),
]