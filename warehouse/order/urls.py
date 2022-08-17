from django.urls import path
from django.urls import include
from rest_framework.routers import SimpleRouter
from .views import OrderViewSet

router = SimpleRouter()
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
