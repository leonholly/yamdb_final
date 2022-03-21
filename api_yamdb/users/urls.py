from django.urls import include, path
from rest_framework import routers

from .views import SignUpViewSet, UserViewSet, get_token

app_name = 'users'


router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'auth/signup', SignUpViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', get_token, name='get_token'),
]
