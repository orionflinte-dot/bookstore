import os
import random
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Category, Book

class Command(BaseCommand):
    help = 'Seed the database with sample categories and beautiful books'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding specific Categories...')
        
        # New Categories
        cat_fantasy, _ = Category.objects.get_or_create(name='Fantasy', slug='fantasy')
        cat_comics, _ = Category.objects.get_or_create(name='Comics', slug='comics')
        cat_indian, _ = Category.objects.get_or_create(name='Indian Fiction', slug='indian-fiction')
        cat_kids, _ = Category.objects.get_or_create(name='Kids Stories', slug='kids-stories')
        cat_classic, _ = Category.objects.get_or_create(name='Classics', slug='classics')

        books_data = [
            # Harry Potter (Fantasy)
            {'title': "Harry Potter and the Sorcerer's Stone", 'author': 'J.K. Rowling', 'price': 499.00, 'category': cat_fantasy, 'description': 'The boy who lived.'},
            {'title': 'Harry Potter and the Chamber of Secrets', 'author': 'J.K. Rowling', 'price': 499.00, 'category': cat_fantasy, 'description': 'Enemies of the heir, beware.'},
            {'title': 'Harry Potter and the Prisoner of Azkaban', 'author': 'J.K. Rowling', 'price': 549.00, 'category': cat_fantasy, 'description': 'The Dementors are coming.'},
            {'title': 'Harry Potter and the Goblet of Fire', 'author': 'J.K. Rowling', 'price': 699.00, 'category': cat_fantasy, 'description': 'The Triwizard Tournament.'},
            {'title': 'Harry Potter and the Order of the Phoenix', 'author': 'J.K. Rowling', 'price': 799.00, 'category': cat_fantasy, 'description': "Dumbledore's Army."},
            {'title': 'Harry Potter and the Half-Blood Prince', 'author': 'J.K. Rowling', 'price': 799.00, 'category': cat_fantasy, 'description': 'The dark secrets revealed.'},
            {'title': 'Harry Potter and the Deathly Hallows', 'author': 'J.K. Rowling', 'price': 899.00, 'category': cat_fantasy, 'description': 'The epic conclusion.'},
            
            # Comics (Marvel/DC)
            {'title': 'Batman: The Killing Joke', 'author': 'Alan Moore', 'price': 1200.00, 'category': cat_comics, 'description': 'One bad day can drive a man crazy.'},
            {'title': 'Superman: Red Son', 'author': 'Mark Millar', 'price': 999.00, 'category': cat_comics, 'description': 'What if Superman was raised in the Soviet Union?'},
            {'title': 'Spider-Man: Kraven\'s Last Hunt', 'author': 'J.M. DeMatteis', 'price': 1100.00, 'category': cat_comics, 'description': 'A grim and iconic Spider-Man tale.'},
            {'title': 'Iron Man: Extremis', 'author': 'Warren Ellis', 'price': 1050.00, 'category': cat_comics, 'description': 'The future of Tony Stark.'},

            # Ruskin Bond
            {'title': 'The Blue Umbrella', 'author': 'Ruskin Bond', 'price': 150.00, 'category': cat_indian, 'description': 'A beautiful story of a young girl in the hills.'},
            {'title': 'The Room on the Roof', 'author': 'Ruskin Bond', 'price': 250.00, 'category': cat_classic, 'description': 'A coming-of-age story of an orphaned English boy in India.'},
            {'title': 'A Flight of Pigeons', 'author': 'Ruskin Bond', 'price': 199.00, 'category': cat_indian, 'description': 'Set against the backdrop of the 1857 rebellion.'},

            # Sudha Murthy
            {'title': "Grandma's Bag of Stories", 'author': 'Sudha Murty', 'price': 200.00, 'category': cat_kids, 'description': 'Magical tales featuring kings, monkeys, and princesses.'},
            {'title': 'Wise and Otherwise', 'author': 'Sudha Murty', 'price': 250.00, 'category': cat_indian, 'description': 'A salute to human nature in all its forms.'},
            {'title': 'How I Taught My Grandmother to Read', 'author': 'Sudha Murty', 'price': 210.00, 'category': cat_indian, 'description': 'Heartwarming stories from real life.'},

            # Kids Story Books
            {'title': 'Panchatantra', 'author': 'Vishnu Sharma', 'price': 300.00, 'category': cat_kids, 'description': 'Ancient Indian fables featuring animals.'},
            {'title': 'The Very Hungry Caterpillar', 'author': 'Eric Carle', 'price': 450.00, 'category': cat_kids, 'description': 'A classic picture book for young children.'},
        ]

        self.stdout.write('Adding Books (Skipping generic images for speed, using fallback styles)...')
        
        # We will use some random beautiful Unsplash URLs for these books to keep the aesthetic!
        unsplash_urls = [
            'https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=600',
            'https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=600',
            'https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600',
            'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600',
            'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=600',
        ]
        
        os.makedirs('media/books', exist_ok=True)

        for i, b_data in enumerate(books_data):
            # Check if book already exists
            if not Book.objects.filter(title=b_data['title']).exists():
                img_url = random.choice(unsplash_urls)
                img_name = f"cover_{i}_{random.randint(1000, 9999)}.jpg"
                img_path = os.path.join('media', 'books', img_name)
                
                try:
                    urllib.request.urlretrieve(img_url, img_path)
                    
                    book = Book(**b_data)
                    with open(img_path, 'rb') as f:
                        book.cover_image.save(img_name, File(f), save=True)
                    self.stdout.write(f"Created: {book.title}")
                except Exception as e:
                    self.stdout.write(f"Failed to create {b_data['title']}: {e}")
            else:
                self.stdout.write(f"Skipping {b_data['title']}, already exists.")

        self.stdout.write(self.style.SUCCESS('Database seeded successfully with requested books!'))
