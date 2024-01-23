from datetime import datetime, timedelta
import random
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.controls.models import Gym, GymPlan
from apps.gym.models import Plan, Subscription, GymSession, QRCode
from apps.users.models import User, GymRole, UserProfile


class Command(BaseCommand):
    help = 'Creates dump data for the app'

    def handle(self, *args, **options):
        self.create_gym_plans()
        self.create_gyms()
        self.create_users()

        self.stdout.write(self.style.SUCCESS(
            'Dump data created successfully!'))

    def create_gym_plans(self):
        GymPlan.objects.create(
            name="Start", description="Standart plan", price=200000, members_limit=50)
        GymPlan.objects.create(
            name="Standart", description="Standart plan", price=500000)
        GymPlan.objects.create(
            name="Premium", description="Premium plan", price=900000)

    def create_gyms(self):
        gym_adjectives = [
            "Powerful",
            "Energetic",
            "Dynamic",
            "Driven",
            "Determined",
            "Unstoppable",
            "Fierce",
            "Strong",
            "Confident",
            "Resilient",
            "Relentless",
            "Passionate",
            "Motivated",
            "Inspiring",
            "Empowering",
            "Transformative",
            "Rewarding",
            "Challenging",
            "Thrilling",
            "Exhilarating",
            "Victorious"
        ]
        gym_nouns = [
            "Challenge",
            "Workout",
            "Session",
            "Routine",
            "Program",
            "Journey",
            "Transformation",
            "Lifestyle",
            "Community",
            "Family",
            "Team",
            "Support",
            "Network",
            "Motivation",
            "Inspiration",
            "Success",
            "Achievement",
            "Goal",
            "Reward",
        ]

        for i in range(1, 51):
            name = f"{random.choice(gym_adjectives)} {random.choice(gym_nouns)} - {i}"
            gym_plans = GymPlan.objects.all()
            gym = Gym.objects.create(
                name=name, gym_plan=random.choice(gym_plans))
            standard_plan = Plan.objects.create(
                name="Стандарт",
                description="Стандартный план",
                price=350000,
                sessions=12,
                gym=gym)
            standard_plan.save()

            vip_plan = Plan.objects.create(
                name="VIP",
                description="VIP план",
                price=400000,
                sessions=31,
                gym=gym)
            vip_plan.save()

    def create_users(self):
        gyms = Gym.objects.all()
        for gym in gyms:
            plans = Plan.objects.filter(gym=gym)
            for _ in range(random.randint(100, 500)):
                phone_number = f"998{random.randint(00, 99)}{random.randint(100000, 9999999)}"
                user = User.objects.filter(phone_number=phone_number).first()
                if user:
                    continue
                user = User.objects.create(
                    phone_number=phone_number,
                    first_name=f"User{random.randint(1, 100)}",
                    last_name=f"Last{random.randint(1, 100)}",
                    is_active=True,
                    is_staff=False,
                )

                UserProfile.objects.create(
                    user=user,
                    weight=random.uniform(50, 100),
                    height=random.uniform(150, 200),
                    biceps=random.uniform(20, 40),
                    triceps=random.uniform(15, 30),
                    chest=random.uniform(70, 120),
                    guts=random.uniform(60, 100),
                    gender=random.choice(['male', 'female']),
                    date_of_birth=timezone.now().date() - timedelta(days=random.randint(365*20, 365*40)),
                    user_type='Member'
                )
                today = timezone.now()
                thirty_days_ago = today - timedelta(days=30)
                start_date = today - \
                    timedelta(seconds=random.randint(
                        0, (today - thirty_days_ago).total_seconds()))
                Subscription.objects.create(
                    member=user,
                    plan=random.choice(plans),
                    status=Subscription.STATUS_CHOICES[0][0],
                    start_date=start_date,
                    end_date=start_date+timedelta(days=30)
                )
