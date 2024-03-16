from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReferralCodeViewSet, SignUPViewSet

router = DefaultRouter()
router.register(r'referral', ReferralCodeViewSet, basename='referral')
router.register(r'sign_up', SignUPViewSet, basename='sign_up')

urlpatterns = [
    path('', include(router.urls)),
]
