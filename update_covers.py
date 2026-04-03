import os
import django
import urllib.request
import json
import time
from urllib.parse import quote
from django.core.files import File


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from store.models import Book

def get_cover_url(title, author):
   
    search_url = f"https://openlibrary.org/search.json?title={quote(title)}&author={quote(author)}"
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get('docs') and len(data['docs']) > 0:
                doc = data['docs'][0]
                cover_i = doc.get('cover_i')
                if cover_i:
                    return f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg"
                
                
                for d in data['docs']:
                    if d.get('cover_i'):
                        return f"https://covers.openlibrary.org/b/id/{d['cover_i']}-L.jpg"
    except Exception as e:
        print(f"OpenLibrary search failed for {title}: {e}")

   
    gb_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{quote(title)}+inauthor:{quote(author)}"
    try:
        req = urllib.request.Request(gb_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get('items'):
                img_links = data['items'][0].get('volumeInfo', {}).get('imageLinks', {})
                if 'thumbnail' in img_links:

                    url = img_links['thumbnail'].replace('http:', 'https:')
                    url = url.replace('&edge=curl', '') 
                    return url.replace('zoom=1', 'zoom=0')
    except Exception as e:
        print(f"Google Books search failed for {title}: {e}")

    return None

def run():
    books = Book.objects.all()
    print(f"Checking covers for {books.count()} books...")
    
    os.makedirs('media/books', exist_ok=True)
    
    for book in books:
        print(f"\nSearching cover for: {book.title} by {book.author}")
        cover_url = get_cover_url(book.title, book.author)
        
        if cover_url:
            print(f"Found cover URL: {cover_url}")
            try:
                
                req = urllib.request.Request(cover_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    img_data = response.read()
                    
                img_name = f"real_cover_{book.id}.jpg"
                img_path = os.path.join('media', 'books', img_name)
                
                with open(img_path, 'wb') as f:
                    f.write(img_data)
                
                with open(img_path, 'rb') as f:
                    
                    if book.cover_image:
                        old_path = book.cover_image.path
                        book.cover_image.delete(save=False)
                        if os.path.exists(old_path):
                            try: os.remove(old_path)
                            except: pass
                    
                    book.cover_image.save(img_name, File(f), save=True)
                    print(f"Successfully updated cover for: {book.title}")
            except Exception as e:
                print(f"Failed to download or save image: {e}")
        else:
            print(f"No real cover found for: {book.title}")
        
       
        time.sleep(1)

if __name__ == '__main__':
    run()
