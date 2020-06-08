from django.conf.urls import url, include
from .views import (RegistrationAPI,
                    LoginAPI, 
                    UserAPI, 
                    RegistrationAPI,
                    UserListAPI,
                    UserUpdateAPI,
                    )

urlpatterns =[
    url("^register/$", RegistrationAPI.as_view()),
    url("^login/$", LoginAPI.as_view()),
    url("^user/$", UserAPI.as_view()),
    url("^update/$", UserUpdateAPI.as_view()),
    url("^userlist/$", UserListAPI.as_view()),
    url("",include("knox.urls")), #logout/ url접속시 로그아웃
]

