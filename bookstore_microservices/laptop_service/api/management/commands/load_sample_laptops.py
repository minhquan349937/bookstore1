from django.core.management.base import BaseCommand
from api.models import Laptop

class Command(BaseCommand):
    help = 'Load sample laptop data'

    def handle(self, *args, **options):
        # Clear existing laptops
        Laptop.objects.all().delete()

        laptops_data = [
            {
                'name': 'MacBook Pro 16',
                'brand': 'Apple',
                'model_name': 'MacBook Pro (16-inch, 2023)',
                'category': 'Ultrabook',
                'processor': 'Apple M3 Max',
                'ram': '36GB',
                'storage': '512GB SSD',
                'display': '16-inch Liquid Retina XDR',
                'gpu': 'Apple M3 Max GPU',
                'price': 45000000,
                'stock': 10,
                'description': 'Professional-grade laptop with exceptional performance and display quality.',
                'image': 'https://www.apple.com/macbook-pro/images/overview/hero__d4d5f9e7yfej.jpg'
            },
            {
                'name': 'XPS 15',
                'brand': 'Dell',
                'model_name': 'Dell XPS 15 (2024)',
                'category': 'Ultrabook',
                'processor': 'Intel Core i9-13900H',
                'ram': '32GB DDR5',
                'storage': '1TB NVMe SSD',
                'display': '15.6-inch OLED',
                'gpu': 'NVIDIA RTX 4080',
                'price': 38000000,
                'stock': 8,
                'description': 'Premium Windows laptop with powerful specs and stunning OLED display.',
                'image': 'https://dell.com/images/products/ddt/xps-15.jpg'
            },
            {
                'name': 'IdeaPad Gaming 3',
                'brand': 'Lenovo',
                'model_name': 'Lenovo IdeaPad Gaming 3 15ACH6',
                'category': 'Gaming',
                'processor': 'AMD Ryzen 7 5800H',
                'ram': '16GB DDR4',
                'storage': '512GB NVMe SSD',
                'display': '15.6-inch 165Hz',
                'gpu': 'NVIDIA RTX 4050',
                'price': 18000000,
                'stock': 15,
                'description': 'Affordable gaming laptop with great performance for gaming and content creation.',
                'image': 'https://lenovo.com/images/gaming-3.jpg'
            },
            {
                'name': 'ROG Strix G16',
                'brand': 'ASUS',
                'model_name': 'ASUS ROG Strix G16 (2024)',
                'category': 'Gaming',
                'processor': 'Intel Core i9-13900HX',
                'ram': '32GB DDR5',
                'storage': '1TB NVMe SSD',
                'display': '16-inch 240Hz',
                'gpu': 'NVIDIA RTX 4090',
                'price': 42000000,
                'stock': 6,
                'description': 'High-end gaming laptop with top-tier performance and immersive display.',
                'image': 'https://asus.com/images/rog-strix-g16.jpg'
            },
            {
                'name': 'Aspire 5 A515-57G',
                'brand': 'Acer',
                'model_name': 'Acer Aspire 5 A515-57G',
                'category': 'Business',
                'processor': 'Intel Core i7-12700H',
                'ram': '16GB DDR4',
                'storage': '512GB NVMe SSD',
                'display': '15.6-inch FHD',
                'gpu': 'NVIDIA RTX 3050',
                'price': 15000000,
                'stock': 12,
                'description': 'Reliable business laptop with balanced performance and affordability.',
                'image': 'https://acer.com/images/aspire-5.jpg'
            },
            {
                'name': 'Prestige 14',
                'brand': 'MSI',
                'model_name': 'MSI Prestige 14 EVO',
                'category': 'Ultrabook',
                'processor': 'Intel Core i7-1360P',
                'ram': '32GB DDR5',
                'storage': '1TB NVMe SSD',
                'display': '14-inch 4K',
                'gpu': 'Intel Iris Xe Graphics',
                'price': 32000000,
                'stock': 5,
                'description': 'Ultra-portable professional laptop with excellent battery life.',
                'image': 'https://msi.com/images/prestige-14.jpg'
            },
            {
                'name': 'Blade 15',
                'brand': 'Razer',
                'model_name': 'Razer Blade 15 (2024)',
                'category': 'Gaming',
                'processor': 'Intel Core i9-13900HX',
                'ram': '32GB DDR5',
                'storage': '1TB NVMe SSD',
                'display': '15.6-inch 240Hz',
                'gpu': 'NVIDIA RTX 4090',
                'price': 48000000,
                'stock': 4,
                'description': 'Ultimate gaming laptop with sleek design and powerful performance.',
                'image': 'https://razer.com/images/blade-15.jpg'
            },
            {
                'name': 'ThinkBook Plus',
                'brand': 'Lenovo',
                'model_name': 'Lenovo ThinkBook Plus Gen 5',
                'category': 'Business',
                'processor': 'Intel Core i7-13700H',
                'ram': '16GB DDR5',
                'storage': '512GB NVMe SSD',
                'display': '14-inch FHD',
                'gpu': 'Intel Iris Xe Graphics',
                'price': 20000000,
                'stock': 8,
                'description': 'Business-focused laptop with productivity features and premium build.',
                'image': 'https://lenovo.com/images/thinkbook-plus.jpg'
            },
            {
                'name': 'Pavilion 15',
                'brand': 'HP',
                'model_name': 'HP Pavilion 15-ec',
                'category': 'Student',
                'processor': 'AMD Ryzen 7 5800H',
                'ram': '8GB DDR4',
                'storage': '256GB SSD',
                'display': '15.6-inch FHD',
                'gpu': 'AMD Radeon Graphics',
                'price': 12000000,
                'stock': 20,
                'description': 'Budget-friendly laptop suitable for students and everyday computing.',
                'image': 'https://hp.com/images/pavilion-15.jpg'
            },
            {
                'name': 'Swift 5',
                'brand': 'Acer',
                'model_name': 'Acer Swift 5 SF514-56T',
                'category': 'Ultrabook',
                'processor': 'Intel Core i7-1360P',
                'ram': '16GB LPDDR5',
                'storage': '512GB NVMe SSD',
                'display': '14-inch FHD',
                'gpu': 'Intel Iris Xe Graphics',
                'price': 22000000,
                'stock': 10,
                'description': 'Ultra-lightweight and portable laptop for professionals on the move.',
                'image': 'https://acer.com/images/swift-5.jpg'
            }
        ]

        for laptop_data in laptops_data:
            laptop = Laptop.objects.create(**laptop_data)
            self.stdout.write(self.style.SUCCESS(f'Created laptop: {laptop.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample laptops'))
