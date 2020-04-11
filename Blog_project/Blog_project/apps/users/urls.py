from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from . import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"blog", views.UserBlogView)

urlpatterns = [
    # url("", views.UserView.as_view()),
    url("^register/$", views.UserView.as_view()),
    url("^sms/$", views.SendSMSView.as_view()),
    url("^login/$", obtain_jwt_token),
    url("^info/$", views.UserDetailInfoView.as_view()),
    url(r"", include(router.urls))
]