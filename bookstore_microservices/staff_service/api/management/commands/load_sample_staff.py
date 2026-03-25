from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Staff

class Command(BaseCommand):
    help = 'Load sample staff data'

    def handle(self, *args, **options):
        # Clear existing staff
        User.objects.filter(username__startswith='staff_').delete()

        staff_data = [
            {
                'username': 'staff_admin',
                'email': 'admin@bookstore.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'password': 'admin123456',
                'staff_info': {
                    'role': 'admin',
                    'phone': '0123456789',
                    'department': 'Management',
                }
            },
            {
                'username': 'staff_manager',
                'email': 'manager@bookstore.com',
                'first_name': 'Manager',
                'last_name': 'User',
                'password': 'manager123456',
                'staff_info': {
                    'role': 'manager',
                    'phone': '0987654321',
                    'department': 'Operations',
                }
            },
            {
                'username': 'staff_librarian1',
                'email': 'librarian1@bookstore.com',
                'first_name': 'Librarian',
                'last_name': 'One',
                'password': 'librarian123456',
                'staff_info': {
                    'role': 'librarian',
                    'phone': '0912345678',
                    'department': 'Library',
                }
            },
            {
                'username': 'staff_librarian2',
                'email': 'librarian2@bookstore.com',
                'first_name': 'Librarian',
                'last_name': 'Two',
                'password': 'librarian123456',
                'staff_info': {
                    'role': 'librarian',
                    'phone': '0911111111',
                    'department': 'Library',
                }
            },
        ]

        count = 0
        for staff in staff_data:
            staff_info = staff.pop('staff_info')
            user = User.objects.create_user(**staff)
            Staff.objects.create(user=user, **staff_info)
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} staff members'))
