from rest_framework.routers import DefaultRouter

from apps.accounts.viewsets.user import AdminUserViewSet
from apps.products.viewsets.brand import BrandViewSet
from apps.products.viewsets.channel import ChannelViewSet
from apps.products.viewsets.price import PriceListViewSet, PriceViewSet
from apps.products.viewsets.product import ProductViewSet

router_v1 = DefaultRouter()
router_v1.register(r"products", ProductViewSet)
router_v1.register(r"brands", BrandViewSet)
router_v1.register(r"accounts", AdminUserViewSet)
router_v1.register(r"prices", PriceViewSet)
router_v1.register(r"prices/channel", PriceListViewSet, basename="price-list")
router_v1.register(r"channels", ChannelViewSet)


urlpatterns_v1 = router_v1.urls
