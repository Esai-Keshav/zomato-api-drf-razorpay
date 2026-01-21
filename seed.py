from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone

from api.models import (
    User,
    Hotel,
    Food,
    DeliveryAgent,
    Order,
    Payment,
    Review,
    Cart,
    CartItem,
    Address,
)
from api.models import OrderStatus, PaymentStatus

fake = Faker()


class Command(BaseCommand):
    help = "Populate database with fake data"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding database...")

        users = self.create_users(10)
        hotels = self.create_hotels(10)
        foods = self.create_foods(hotels)
        agents = self.create_delivery_agents(5)

        self.create_addresses(users)
        self.create_carts(users, foods)
        self.create_orders(users, foods, agents)
        self.create_reviews(users, hotels, foods)

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully"))

    # ---------- USERS ----------
    def create_users(self, count):
        users = []
        for i in range(count):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
                phone_number=fake.msisdn()[:10],
                address=fake.address(),
            )
            users.append(user)
        return users

    # ---------- HOTELS ----------
    def create_hotels(self, count):
        hotels = []
        for _ in range(count):
            hotel = Hotel.objects.create(
                name=fake.company(),
                address=fake.address(),
                city=fake.city(),
                image_url=fake.image_url(),
            )
            hotels.append(hotel)
        return hotels

    # ---------- FOODS ----------
    def create_foods(self, hotels):
        foods = []
        food_types = ["veg", "non-veg", "vegan"]

        for hotel in hotels:
            for _ in range(10):  # 10 food per hotel
                food = Food.objects.create(
                    hotel=hotel,
                    name=fake.word().title(),
                    price=random.randint(100, 500),
                    food_type=random.choice(food_types),
                    image=fake.image_url(),
                )
                foods.append(food)
        return foods

    # ---------- DELIVERY AGENTS ----------
    def create_delivery_agents(self, count):
        agents = []
        for _ in range(count):
            agent = DeliveryAgent.objects.create(
                name=fake.name(),
                phone_number=fake.msisdn()[:10],
                vehicle_number=fake.license_plate(),
            )
            agents.append(agent)
        return agents

    # ---------- ADDRESSES ----------
    def create_addresses(self, users):
        for user in users:
            Address.objects.create(
                user=user,
                label="Home",
                address_line=fake.address(),
                city=fake.city(),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                is_default=True,
            )

    # ---------- CARTS & CART ITEMS ----------
    def create_carts(self, users, foods):
        for user in users:
            cart, _ = Cart.objects.get_or_create(user=user)
            for food in random.sample(foods, 5):
                CartItem.objects.create(
                    cart=cart,
                    food=food,
                    quantity=random.randint(1, 3),
                )

    # ---------- ORDERS ----------
    def create_orders(self, users, foods, agents):
        for _ in range(15):
            user = random.choice(users)
            selected_foods = random.sample(foods, 3)
            total_price = sum(food.price for food in selected_foods)

            order = Order.objects.create(
                user=user,
                delivery_agent=random.choice(agents),
                status=random.choice(OrderStatus.values),
                total_price=total_price,
            )

            Payment.objects.create(
                order=order,
                payment_id=fake.uuid4(),
                amount=total_price,
                status=random.choice(PaymentStatus.values),
                paid_at=timezone.now(),
            )

    # ---------- REVIEWS ----------
    def create_reviews(self, users, hotels, foods):
        for _ in range(20):
            Review.objects.create(
                user=random.choice(users),
                hotel=random.choice(hotels),
                food=random.choice(foods),
                rating=random.uniform(3, 5),
                comment=fake.sentence(),
            )
