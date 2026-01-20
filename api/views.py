from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomer, IsHotelOwner
from rest_framework.response import Response
from .serializers import (
    HotelSerialer,
    UserSerializer,
    FoodSerializer,
    DeliveryAgentSerializer,
    OrderSerializer,
    ReviewSerializer,
    AddressSerializer,
    PaymentSerializer,
    CartItemSerializer,
)

from .models import (
    Hotel,
    User,
    Food,
    DeliveryAgent,
    Order,
    Review,
    Address,
    Payment,
    CartItem,
)
from .pay import get_url, payment_status
from datetime import datetime


@api_view(["GET"])
def health(request):
    # print(request.body)
    return Response({"status": "API is working"})


class HotelAPI(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerialer

    @action(detail=True, methods=["get"])
    def foods(self, request, pk=None):
        # print(request.user)
        hotel = self.get_object()
        foods = hotel.foods.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        hotel = self.get_object()
        reviews = hotel.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        print(serializer.data)
        return Response(serializer.data)


class UserAPI(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FoodAPI(ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    # permission_classes = [IsAuthenticated & (IsCustomer | IsHotelOwner)]

    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        print(self.request.user, "<<")
        food = self.get_object()
        reviews = food.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        print(serializer.data)
        return Response(serializer.data)


class DeliveryAgentAPI(ModelViewSet):
    queryset = DeliveryAgent.objects.all()
    serializer_class = DeliveryAgentSerializer


# class OrderAPI(ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer


#     # permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     return Order.objects.filter(user=self.request.user)


class OrderAPI(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     print(self.request.user, "= user")
    #     return Order.objects.filter(user=self.request.user)

    @action(detail=True, methods=["get"])
    def pay(self, request, pk=None):
        order = self.get_object()
        print(order)

        price = float(OrderSerializer(order).data["total_price"])
        # return Response({"ok": "ok"})
        print(price)

        return Response(get_url(price, order_id=order.id))
        # return get_url((OrderSerializer(order).data["total_price"]))


class ReviewAPI(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = OrderSerializer


class AddressAPI(ModelViewSet):
    # queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        # print(self.request.query_params.get("id"))
        # print(Address.objects.filter(user=self.request.user))
        return Address.objects.filter(user=self.request.user)


class PaymentAPI(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    # def get_queryset(self):
    #     id = self.request.query_params.get("id")
    #     return Payment.objects.filter(id=id)

    @action(detail=False, methods=["get"])
    def callback(self, request, pk=None):
        print(request, "<<")
        # print(self.get_object())
        pay_id = self.request.query_params.get("razorpay_payment_id")
        status = self.request.query_params.get("razorpay_payment_link_status")
        res = payment_status(pay_id)
        # print(res["created_at"])
        order_id = res["notes"]["order_id"]
        order = Order.objects.get(id=order_id)

        Payment.objects.create(
            order=order,
            payment_id=pay_id,
            amount=res["amount"],
            status=status,
            paid_at=datetime.fromtimestamp(
                res["created_at"],
            ),
        )

        return Response({"razorpay_id": pay_id, "payment_status": status, "api": res})


class CartItemAPI(ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
