from rest_framework.routers import DefaultRouter


from products.viewsets import ProductViewSet, ProductGenericViewSet

router = DefaultRouter()
router.register('products', ProductGenericViewSet, basename='products')

urlpatterns = router.urls

"""
  The bad side to use this approach is does not provide the granular control
  that separate views can have, but for simple crud operations is fine
"""
