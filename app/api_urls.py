from rest_framework.routers import DefaultRouter
from .api_views import OrderViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')

urlpatterns = router.urls
