import os
import django
import json
from django.core import serializers

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from store.models import Book, Category

def export_data():
    print("🧹 Cleaning and exporting your books...")
    
    # We only need Books and Categories for the live site
    queryset = list(Category.objects.all()) + list(Book.objects.all())
    
    data = serializers.serialize("json", queryset, indent=2)
    
    # Save with forced UTF-8 encoding
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(data)
        
    print(f"✅ Successfully exported {len(queryset)} objects to data.json")

if __name__ == "__main__":
    export_data()
