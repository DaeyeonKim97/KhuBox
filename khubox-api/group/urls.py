from django.conf.urls import url, include
from .views import (
                        CreateGroupAPI,
                        GroupListAPI,
                        AddUserAPI
                    )

urlpatterns =[
    url("^creategroup/$", CreateGroupAPI.as_view()),
    url("^grouplist/$", GroupListAPI.as_view()),
    url("^adduser/$", AddUserAPI.as_view()),
]
