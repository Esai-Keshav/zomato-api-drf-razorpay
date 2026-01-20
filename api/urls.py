from rest_framework.routers import DefaultRouter
from .views import (
    HotelAPI,
    UserAPI,
    FoodAPI,
    DeliveryAgentAPI,
    OrderAPI,
    AddressAPI,
    PaymentAPI,
    CartItemAPI,
    health,
)
from django.urls import path, include


router = DefaultRouter()

router.register("hotels", HotelAPI, basename="Hotel API")
router.register("users", UserAPI, basename="User API")
router.register("foods", FoodAPI, basename="Food API")
router.register("agents", DeliveryAgentAPI, basename="Agent API")
router.register("orders", OrderAPI, basename="Order API")
router.register("address", AddressAPI, basename="Address API")
router.register("payment", PaymentAPI, basename="Payment API")
# router.register("health", health, basename="Health API")
# router.register("cart", CartItemAPI, basename="Cart Item API")

urlpatterns = [
    path("", include(router.urls)),
    path("health/", health),
]

# print(router.urls)
