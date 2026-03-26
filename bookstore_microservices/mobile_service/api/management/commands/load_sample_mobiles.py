from django.core.management.base import BaseCommand
from api.models import Mobile

class Command(BaseCommand):
    help = 'Load sample mobile data'

    def handle(self, *args, **options):
        # Clear existing mobiles
        Mobile.objects.all().delete()

        mobiles_data = [
            {
                'name': 'iPhone 15 Pro Max',
                'brand': 'Apple',
                'model_name': 'iPhone 15 Pro Max',
                'os': 'iOS',
                'processor': 'Apple A17 Pro',
                'ram': '8GB',
                'storage': '256GB',
                'display': '6.7-inch Super Retina XDR',
                'camera': '12MP+12MP+12MP Triple Camera',
                'battery': '4685 mAh',
                'price': 32000000,
                'stock': 15,
                'description': 'Latest flagship iPhone with advanced camera system and A17 Pro chip.',
                'image': 'https://images.unsplash.com/photo-1592286927505-1def25e246c0?w=500&h=400&fit=crop'
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'brand': 'Samsung',
                'model_name': 'Samsung Galaxy S24 Ultra',
                'os': 'Android',
                'processor': 'Snapdragon 8 Gen 3',
                'ram': '12GB',
                'storage': '256GB',
                'display': '6.8-inch Dynamic AMOLED 2X',
                'camera': '200MP+50MP+10MP+10MP Quad Camera',
                'battery': '5000 mAh',
                'price': 28000000,
                'stock': 12,
                'description': 'Premium Android flagship with powerful processor and exceptional camera.',
                'image': 'https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=500&h=400&fit=crop'
            },
            {
                'name': 'Pixel 8 Pro',
                'brand': 'Google',
                'model_name': 'Google Pixel 8 Pro',
                'os': 'Android',
                'processor': 'Google Tensor G3',
                'ram': '12GB',
                'storage': '128GB',
                'display': '6.7-inch AMOLED',
                'camera': '50MP+48MP+48MP Triple Camera',
                'battery': '5050 mAh',
                'price': 24000000,
                'stock': 10,
                'description': 'Google flagship with advanced AI features and excellent computational photography.',
                'image': 'https://images.unsplash.com/photo-1606933248051-5ce98becdc2e?w=500&h=400&fit=crop'
            },
            {
                'name': 'OnePlus 12',
                'brand': 'OnePlus',
                'model_name': 'OnePlus 12',
                'os': 'Android',
                'processor': 'Snapdragon 8 Gen 3',
                'ram': '16GB',
                'storage': '256GB',
                'display': '6.7-inch AMOLED 120Hz',
                'camera': '50MP+48MP+48MP Triple Camera',
                'battery': '5400 mAh',
                'price': 18000000,
                'stock': 14,
                'description': 'Fast and smooth Android phone with excellent performance.',
                'image': 'https://images.unsplash.com/photo-1551431009-381d36d3d37d?w=500&h=400&fit=crop'
            },
            {
                'name': 'Xiaomi 14 Ultra',
                'brand': 'Xiaomi',
                'model_name': 'Xiaomi 14 Ultra',
                'os': 'Android',
                'processor': 'Snapdragon 8 Gen 3 Leading Version',
                'ram': '16GB',
                'storage': '512GB',
                'display': '6.73-inch AMOLED 120Hz',
                'camera': '50MP+50MP+50MP Triple Camera',
                'battery': '5500 mAh',
                'price': 22000000,
                'stock': 8,
                'description': 'Chinese flagship with incredible camera setup and high-end specs.',
                'image': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&h=400&fit=crop'
            },
            {
                'name': 'OPPO Find X7',
                'brand': 'OPPO',
                'model_name': 'OPPO Find X7',
                'os': 'Android',
                'processor': 'Snapdragon 8 Gen 3',
                'ram': '16GB',
                'storage': '512GB',
                'display': '6.78-inch AMOLED 120Hz',
                'camera': '50MP+50MP Dual Camera',
                'battery': '5910 mAh',
                'price': 20000000,
                'stock': 10,
                'description': 'Premium Android phone with exceptional camera and fast charging.',
                'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=400&fit=crop'
            },
            {
                'name': 'Vivo X100 Ultra',
                'brand': 'Vivo',
                'model_name': 'Vivo X100 Ultra',
                'os': 'Android',
                'processor': 'Snapdragon 8 Gen 3 Leading Version',
                'ram': '16GB',
                'storage': '512GB',
                'display': '6.82-inch AMOLED 120Hz',
                'camera': '50MP+50MP+50MP Triple Camera',
                'battery': '6000 mAh',
                'price': 21000000,
                'stock': 9,
                'description': 'Latest Vivo flagship with excellent performance and camera.',
                'image': 'https://images.unsplash.com/photo-1511454576620-ba8a36ffac77?w=500&h=400&fit=crop'
            },
            {
                'name': 'Realme GT 5 Pro',
                'brand': 'Realme',
                'model_name': 'Realme GT 5 Pro',
                'os': 'Android',
                'processor': 'Snapdragon 8 Gen 3',
                'ram': '12GB',
                'storage': '256GB',
                'display': '6.7-inch AMOLED 120Hz',
                'camera': '50MP+50MP Dual Camera',
                'battery': '5800 mAh',
                'price': 15000000,
                'stock': 16,
                'description': 'Value-for-money flagship with solid performance.',
                'image': 'https://images.unsplash.com/photo-1578149102327-636b7834603f?w=500&h=400&fit=crop'
            },
            {
                'name': 'Samsung Galaxy A54',
                'brand': 'Samsung',
                'model_name': 'Samsung Galaxy A54',
                'os': 'Android',
                'processor': 'Exynos 1380',
                'ram': '8GB',
                'storage': '128GB',
                'display': '6.4-inch AMOLED',
                'camera': '50MP+12MP+5MP Triple Camera',
                'battery': '5000 mAh',
                'price': 10500000,
                'stock': 20,
                'description': 'Mid-range Samsung phone suitable for everyday use.',
                'image': 'https://images.unsplash.com/photo-1511385643326-ab7782d7ad18?w=500&h=400&fit=crop'
            },
            {
                'name': 'iPhone 14',
                'brand': 'Apple',
                'model_name': 'iPhone 14',
                'os': 'iOS',
                'processor': 'Apple A15 Bionic',
                'ram': '6GB',
                'storage': '128GB',
                'display': '6.1-inch Super Retina XDR',
                'camera': '12MP+12MP Dual Camera',
                'battery': '3279 mAh',
                'price': 22000000,
                'stock': 18,
                'description': 'Previous generation iPhone still offering great performance and features.',
                'image': 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=500&h=400&fit=crop'
            }
        ]

        for mobile_data in mobiles_data:
            mobile = Mobile.objects.create(**mobile_data)
            self.stdout.write(self.style.SUCCESS(f'Created mobile: {mobile.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample mobiles'))
