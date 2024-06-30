from rest_framework.routers import DefaultRouter
from django.urls import path

from logistic.views import ProductViewSet, StockViewSet, test_view

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('stocks', StockViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('test/', test_view, name='test_view'),
]
