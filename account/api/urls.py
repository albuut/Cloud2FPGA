from django.urls import path

from django.conf.urls import url, include
from .views import GameViewSet,UserGameViewSet
from rest_framework.routers import DefaultRouter

from account.api.views import(
    registration_view,
)

from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register("usergameinfo", UserGameViewSet, basename="usergameinfo")
router.register("gameinfo",GameViewSet, basename="gameinfo")


app_name = "account"

urlpatterns = [
    url('',include(router.urls)),
    path('register', registration_view, name = 'register'),
    path('login', obtain_auth_token, name = 'login')
]


