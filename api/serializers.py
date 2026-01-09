from rest_framework import serializers
from .models import (
    Hotel,
    User,
    Food,
    DeliveryAgent,
    Payment,
    Order,
    Review,
    Address,
    Cart,
    CartItem,
)


class HotelSerialer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ["id", "username", "address", "phone_number", "email"]


class FoodSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField()

    class Meta:
        model = Food
        fields = "__all__"


class DeliveryAgentSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField()

    class Meta:
        model = DeliveryAgent
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    hotel = serializers.StringRelatedField()
    delivery_agent = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField()
    order = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.StringRelatedField()
    food = serializers.StringRelatedField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_total_price(self, obj):
        return obj.food.price * obj.quantity
