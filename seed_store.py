import os
import django
import urllib.request
import random
from django.core.files import File

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Book, Category

def run_seed():
    print("🌱 Starting premium store seeding...")
    
    # 1. Define Categories
    categories_data = [
        {'name': 'Technology', 'slug': 'technology'},
        {'name': 'Fiction', 'slug': 'fiction'},
        {'name': 'Wellness', 'slug': 'wellness'},
        {'name': 'Business', 'slug': 'business'},
        {'name': 'Digital E-Books', 'slug': 'digital-e-books'},
    ]

    categories = {}
    for cat in categories_data:
        c, _ = Category.objects.get_or_create(name=cat['name'], slug=cat['slug'])
        categories[cat['name']] = c

    # 2. Define Books Data
    books_data = [
        # Technology
        {'title': 'Artificial Intelligence: A Modern Approach', 'author': 'Russell & Norvig', 'price': 89.99, 'cat': 'Technology', 'is_ebook': False},
        {'title': 'Clean Code', 'author': 'Robert C. Martin', 'price': 45.50, 'cat': 'Technology', 'is_ebook': False},
        {'title': 'Rust Programming', 'author': 'Steve Klabnik', 'price': 39.99, 'cat': 'Technology', 'is_ebook': True},
        
        # Fiction
        {'title': 'The Midnight Library', 'author': 'Matt Haig', 'price': 18.00, 'cat': 'Fiction', 'is_ebook': False},
        {'title': 'Circe', 'author': 'Madeline Miller', 'price': 16.50, 'cat': 'Fiction', 'is_ebook': False},
        {'title': 'Klara and the Sun', 'author': 'Kazuo Ishiguro', 'price': 14.99, 'cat': 'Fiction', 'is_ebook': True},
        
        # Wellness
        {'title': 'Atomic Habits', 'author': 'James Clear', 'price': 22.00, 'cat': 'Wellness', 'is_ebook': False},
        {'title': 'The Body Keeps the Score', 'author': 'Bessel van der Kolk', 'price': 25.00, 'cat': 'Wellness', 'is_ebook': False},
        {'title': 'Mindfulness in Plain English', 'author': 'Bhante Gunaratana', 'price': 12.99, 'cat': 'Wellness', 'is_ebook': True},
        
        # Business
        {'title': 'Zero to One', 'author': 'Peter Thiel', 'price': 28.00, 'cat': 'Business', 'is_ebook': False},
        {'title': 'Thinking, Fast and Slow', 'author': 'Daniel Kahneman', 'price': 32.00, 'cat': 'Business', 'is_ebook': False},
        {'title': 'The Lean Startup', 'author': 'Eric Ries', 'price': 19.99, 'cat': 'Business', 'is_ebook': True},
    ]

    # Covers from Unsplash
    covers = [
        'https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=600',
        'https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=600',
        'https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600',
        'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?q=80&w=600',
        'https://images.unsplash.com/photo-1589998059171-988d887df646?q=80&w=600'
    ]

    os.makedirs('media/books', exist_ok=True)
    os.makedirs('media/ebooks', exist_ok=True)

    for i, b_data in enumerate(books_data):
        book, created = Book.objects.get_or_create(
            title=b_data['title'],
            defaults={
                'author': b_data['author'],
                'price': b_data['price'],
                'description': f"A must-read masterpiece in {b_data['cat']}. Highly recommended for all readers.",
                'category': categories[b_data['cat']],
                'is_ebook': b_data['is_ebook'],
                'stock': random.randint(10, 50)
            }
        )

        if not book.cover_image:
            img_url = random.choice(covers)
            img_name = f"cover_{i}_{random.randint(100,999)}.jpg"
            img_path = os.path.join('media/books', img_name)
            try:
                urllib.request.urlretrieve(img_url, img_path)
                with open(img_path, 'rb') as f:
                    book.cover_image.save(img_name, File(f), save=True)
            except: pass

        print(f"✅ Added: {book.title}")

    print("✨ Seeding complete!")

if __name__ == '__main__':
    run_seed()
