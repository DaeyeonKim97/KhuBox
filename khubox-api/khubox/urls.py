from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^folders/(?P<pk>\w+)/$', views.FolderRequest.as_view()),
    url(r'^folders/$', views.FolderRequest.as_view()),
    url(r'^files/', views.StarredFiles.as_view()),
    url(r'^files/starred/(?P<pk>\w+).$', views.StarredFiles.as_view()),
    url(r'^trash/(?P<pk>\w+)/$', views.TrashReqeust.as_view()),
    url(r'^trash/$', views.FolderRequest.as_view()),
])