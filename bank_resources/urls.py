from rest_framework import routers
from .api import AccountViewSet, AccountTypeViewSet, AccountStatusViewSet, LoanViewSet, StatusLoanViewSet

router = routers.DefaultRouter()

router.register("account", AccountViewSet, "account")
router.register("account-type", AccountTypeViewSet, "account-type")
router.register("account-status", AccountStatusViewSet, "account-status")
router.register("loan", LoanViewSet, "loan")
router.register("status-loan", StatusLoanViewSet, "status-loan")

urlpatterns = router.urls
