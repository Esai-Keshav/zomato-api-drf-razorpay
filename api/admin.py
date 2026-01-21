from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Hotel,
    User,
    DeliveryAgent,
    Food,
    Review,
    Order,
    Payment,
    Address,
    Cart,
    CartItem,
)


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("phone_number", "address")}),
    )

    list_display = ("username", "email", "phone_number", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number")


# Register your models here.
admin.site.register(Hotel)
admin.site.register(DeliveryAgent)
admin.site.register(Food)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(CartItem)
admin.site.register(Cart)
