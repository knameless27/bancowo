from rest_framework import routers
from .api import LoginViewSet, UserViewSet, RegisterViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet, 'users')
router.register('login', LoginViewSet, 'login')
router.register('register', RegisterViewSet, 'register')
urlpatterns = router.urls
