from django.core.management.base import BaseCommand
from api.models import Book

class Command(BaseCommand):
    help = 'Load sample book data'

    def handle(self, *args, **options):
        # Clear existing books
        Book.objects.all().delete()

        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'publisher': 'Scribner',
                'genre': 'Fiction',
                'year': 1925,
                'pages': 180,
                'isbn': '978-0143039990',
                'price': 299000,
                'stock': 25,
                'description': 'A classic American novel set in the Jazz Age.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0143039990.01.LZZZZZZZ.jpg'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'publisher': 'J.B. Lippincott',
                'genre': 'Fiction',
                'year': 1960,
                'pages': 324,
                'isbn': '978-0061120084',
                'price': 325000,
                'stock': 30,
                'description': 'A gripping tale of racial injustice and childhood innocence.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0061120084.01.LZZZZZZZ.jpg'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'publisher': 'Signet',
                'genre': 'Science Fiction',
                'year': 1949,
                'pages': 328,
                'isbn': '978-0451524935',
                'price': 275000,
                'stock': 20,
                'description': 'A dystopian masterpiece about totalitarianism.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0451524934.01.LZZZZZZZ.jpg'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'publisher': 'Penguin Classics',
                'genre': 'Romance',
                'year': 1813,
                'pages': 432,
                'isbn': '978-0141439518',
                'price': 285000,
                'stock': 28,
                'description': 'A romantic masterpiece about love and social class.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0141439513.01.LZZZZZZZ.jpg'
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'publisher': 'Little, Brown',
                'genre': 'Fiction',
                'year': 1951,
                'pages': 277,
                'isbn': '978-0316769174',
                'price': 295000,
                'stock': 22,
                'description': 'A coming-of-age story narrated by a teenage rebel.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0316769177.01.LZZZZZZZ.jpg'
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'publisher': 'Prentice Hall',
                'genre': 'Technology',
                'year': 2008,
                'pages': 464,
                'isbn': '978-0132350884',
                'price': 450000,
                'stock': 15,
                'description': 'A handbook of agile software craftsmanship.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0132350882.01.LZZZZZZZ.jpg'
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt',
                'publisher': 'Addison-Wesley',
                'genre': 'Technology',
                'year': 1999,
                'pages': 321,
                'isbn': '978-0135957059',
                'price': 425000,
                'stock': 18,
                'description': 'Your journey to mastery in software development.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0135957052.01.LZZZZZZZ.jpg'
            },
            {
                'title': 'The Da Vinci Code',
                'author': 'Dan Brown',
                'publisher': 'Doubleday',
                'genre': 'Mystery',
                'year': 2003,
                'pages': 689,
                'isbn': '978-0307474278',
                'price': 335000,
                'stock': 20,
                'description': 'A fast-paced mystery involving ancient symbols and secrets.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0307474275.01.LZZZZZZZ.jpg'
            },
            {
                'title': 'Sapiens',
                'author': 'Yuval Noah Harari',
                'publisher': 'Harper',
                'genre': 'History',
                'year': 2011,
                'pages': 512,
                'isbn': '978-0062316097',
                'price': 380000,
                'stock': 24,
                'description': 'A brief history of mankind from the Stone Age to modern times.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/0062316095.01.LZZZZZZZ.jpg'
            },
            {
                'title': 'Steve Jobs',
                'author': 'Walter Isaacson',
                'publisher': 'Simon & Schuster',
                'genre': 'Biography',
                'year': 2011,
                'pages': 656,
                'isbn': '978-1451648539',
                'price': 390000,
                'stock': 16,
                'description': 'An authorized biography of Steve Jobs.',
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/P/1451648537.01.LZZZZZZZ.jpg'
            },
        ]

        for book_data in books_data:
            Book.objects.create(**book_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(books_data)} books'))
