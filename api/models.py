from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=True)
    address = models.TextField(blank=True)


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.city} "


class Food(models.Model):
    FOOD_TYPE_CHOICES = [
        ("veg", "Veg"),
        ("non-veg", "Non-Veg"),
        ("vegan", "Vegan"),
    ]

    hotel = models.ForeignKey(Hotel, related_name="foods", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES)
    # image = models.ImageField(upload_to="food_images/", null=True, blank=True)
    image = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} [{self.hotel}]"


class DeliveryAgent(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    vehicle_number = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class OrderStatus(models.TextChoices):
    ORDERED = "ordered", "Ordered"
    PREPARING = "preparing", "Preparing"
    PICKED_UP = "picked_up", "Picked Up"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    delivery_agent = models.ForeignKey(
        DeliveryAgent, null=True, blank=True, on_delete=models.SET_NULL
    )

    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.ORDERED
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f" ${self.amount / 100} ? {self.status}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="reviews")
    food = models.ForeignKey(
        Food, null=True, blank=True, on_delete=models.SET_NULL, related_name="reviews"
    )

    rating = models.FloatField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating = {self.rating} [{self.hotel}] {self.food or ''}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cart", "food")

    def __str__(self):
        return f"{self.cart} items"


# class Favorite(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     hotel = models.ForeignKey(Hotel, null=True, blank=True, on_delete=models.CASCADE)
#     food = models.ForeignKey(Food, null=True, blank=True, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ("user", "hotel", "food")


class Address(models.Model):
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    label = models.CharField(max_length=50)  # Home / Office
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} | {self.city}"


# class MembershipPlan(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     duration_days = models.PositiveIntegerField()
#     benefits = models.TextField()


# class UserMembership(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     is_active = models.BooleanField(default=True)


# class Address(models.Model):
#     user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
#     label = models.CharField(max_length=50)  # Home / Office
#     address_line = models.TextField()
#     city = models.CharField(max_length=100)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     is_default = models.BooleanField(default=False)
