from rest_framework import routers
from django.urls import path
from cash_machine.views import ItemViewSet, CashMachineAPIView, MediaAPIView

router = routers.DefaultRouter()
router.register(r'items', viewset=ItemViewSet)
urlpatterns = [
    path('cash_machine/', CashMachineAPIView.as_view(), name='media'),
    path('media/<str:filename>/', MediaAPIView.as_view(), name='media'),
]