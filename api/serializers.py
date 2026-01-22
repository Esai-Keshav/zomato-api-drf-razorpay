from rest_framework import serializers
from django.contrib.auth.models import User
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
    # hotel = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ["id", "username", "address", "phone_number", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # 🔐 hashing happens here
        user.save()
        Cart.objects.create(user=user)
        return user


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
    # hotel = hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    delivery_agent = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["user"]


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


# class CartItemSerializer(serializers.ModelSerializer):
#     cart = serializers.StringRelatedField()
#     food = serializers.StringRelatedField()
#     # food_image = serializers.SerializerMethodField()
#     total_price = serializers.SerializerMethodField()

#     class Meta:
#         model = CartItem
#         fields = ["food", "quantity", "cart"]
#         # read_only_fields = ["food_image"]

#     def get_total_price(self, obj):
#         return obj.food.price * obj.quantity

#     def get_food_image(self, obj):
#         return obj.food.image


class CartItemSerializer(serializers.ModelSerializer):
    # WRITE: accept food ID
    food = serializers.PrimaryKeyRelatedField(
        queryset=Food.objects.all(), write_only=True
    )

    # READ: derived fields
    food_name = serializers.CharField(source="food.name", read_only=True)
    food_image = serializers.URLField(source="food.image", read_only=True)
    food_price = serializers.DecimalField(
        source="food.price", max_digits=8, decimal_places=2, read_only=True
    )

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "food",  # for POST
            "food_name",  # for GET
            "food_image",
            "food_price",
            "quantity",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.food.price * obj.quantity

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        cart, _ = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            food=validated_data["food"],
            defaults={"quantity": validated_data["quantity"]},
        )

        if not created:
            cart_item.quantity += validated_data["quantity"]
            cart_item.save()

        return cart_item
