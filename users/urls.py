from rest_framework import routers
from .api import UserViewSet, RegisterViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet, 'users')

router.register('register', RegisterViewSet, 'register')
urlpatterns = router.urls
