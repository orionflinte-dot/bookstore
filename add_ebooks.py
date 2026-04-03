import os
import django
import urllib.request
import random
from django.core.files import File

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Book, Category

def run():
    print("Adding 5 Digital eBooks...")
    cat_ebook, _ = Category.objects.get_or_create(name='Digital E-Books', slug='digital-e-books')
    
    os.makedirs('media/ebooks', exist_ok=True)
    pdf_path = 'media/ebooks/sample_ebook.pdf'
    
    # Download a tiny dummy PDF to serve as the eBook file
    try:
        urllib.request.urlretrieve('https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf', pdf_path)
    except Exception as e:
        print(f"Failed to download dummy pdf, creating a txt file instead: {e}")
        pdf_path = 'media/ebooks/sample_ebook.txt'
        with open(pdf_path, 'w') as f:
            f.write("This is a sample eBook content for testing!")

    # Fetch some random cover images for them too
    unsplash_urls = [
        'https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=600',
        'https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=600',
        'https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600',
    ]

    ebooks_data = [
        {'title': 'Python Web Development (eBook)', 'author': 'Aura Experts', 'price': 299.00, 'description': 'Learn to build modern apps in Python.', 'is_ebook': True},
        {'title': 'Modern CSS & Glassmorphism (eBook)', 'author': 'Design Team', 'price': 199.00, 'description': 'Advanced styling strategies for 2026.', 'is_ebook': True},
        {'title': 'The Digital Minimalism (eBook)', 'author': 'Tech Writers', 'price': 149.00, 'description': 'Organize your digital life effectively.', 'is_ebook': True},
        {'title': 'Django Advanced Guide (eBook)', 'author': 'Backend Experts', 'price': 499.00, 'description': 'Deep dive into Django structure.', 'is_ebook': True},
        {'title': 'Startup Funding 101 (eBook)', 'author': 'VC Mentors', 'price': 399.00, 'description': 'How to pitch and win investments.', 'is_ebook': True},
    ]

    os.makedirs('media/books', exist_ok=True)

    for i, ed in enumerate(ebooks_data):
        b, created = Book.objects.get_or_create(title=ed['title'], defaults={
            'author': ed['author'], 
            'price': ed['price'], 
            'description': ed['description'], 
            'is_ebook': ed['is_ebook'], 
            'category': cat_ebook
        })
        
        # Attach eBook file
        if not b.e_book_file:
            with open(pdf_path, 'rb') as f:
                b.e_book_file.save('sample_ebook.pdf', File(f), save=False)
                
        # Attach Cover image
        if not b.cover_image:
            img_url = random.choice(unsplash_urls)
            img_name = f"ebook_cover_{i}_{random.randint(1000, 9999)}.jpg"
            img_path = os.path.join('media', 'books', img_name)
            try:
                urllib.request.urlretrieve(img_url, img_path)
                with open(img_path, 'rb') as img_f:
                    b.cover_image.save(img_name, File(img_f), save=False)
            except Exception as e:
                pass
                
        b.save()
        print(f"Added eBook: {b.title}")

if __name__ == '__main__':
    run()
