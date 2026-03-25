from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import CustomerProfile

class Command(BaseCommand):
    help = 'Load sample customer data'

    def handle(self, *args, **options):
        # Clear existing customers
        User.objects.filter(username__startswith='customer_').delete()

        customers_data = [
            {
                'username': 'customer_1',
                'email': 'customer1@email.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'gfi',
                'profile': {
                    'phone': '0123456789',
                    'address': '123 Main Street',
                    'city': 'Ho Chi Minh City',
                    'country': 'Vietnam',
                }
            },
            {
                'username': 'customer_2',
                'email': 'customer2@email.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'password': 'gfi',
                'profile': {
                    'phone': '0987654321',
                    'address': '456 Oak Avenue',
                    'city': 'Hanoi',
                    'country': 'Vietnam',
                }
            },
            {
                'username': 'customer_3',
                'email': 'customer3@email.com',
                'first_name': 'Bob',
                'last_name': 'Johnson',
                'password': 'gfi',
                'profile': {
                    'phone': '0912345678',
                    'address': '789 Pine Road',
                    'city': 'Da Nang',
                    'country': 'Vietnam',
                }
            },
        ]

        count = 0
        for customer_data in customers_data:
            profile_data = customer_data.pop('profile')
            user = User.objects.create_user(**customer_data)
            CustomerProfile.objects.create(user=user, **profile_data)
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} customers'))
