from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Book, Category, Cart, CartItem, Order

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def home(request):
    featured_books = Book.objects.filter(is_active=True).order_by('-created_at')[:4]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'featured_books': featured_books, 'categories': categories})

def book_list(request):
    books = Book.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    categories = Category.objects.all()
    
    if category_slug:
        books = books.filter(category__slug=category_slug)
        
    if search_query:
        books = books.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
        
    return render(request, 'store/book_list.html', {'books': books, 'categories': categories, 'search_query': search_query})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id, is_active=True)
    return render(request, 'store/book_detail.html', {'book': book})

def cart_detail(request):
    cart = get_or_create_cart(request)
    items = cart.items.all()
    total = sum(item.book.price * item.quantity for item in items)
    return render(request, 'store/cart.html', {'cart': cart, 'items': items, 'total': total})

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('store:cart_detail')

@login_required(login_url='/login/')
def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.all()
    if not items.exists():
        return redirect('store:home')
    
    total = sum(item.book.price * item.quantity for item in items)
    
    if request.method == 'POST':
        # Mocking the checkout process
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            zip_code=request.POST.get('zip_code'),
            total_price=total,
            is_paid=True
        )
        # Clear cart
        cart.items.all().delete()
        return redirect('store:checkout_success')

    return render(request, 'store/checkout.html', {'items': items, 'total': total})

def checkout_success(request):
    return render(request, 'store/checkout_success.html')



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()
            
            # Send Email Verification
            current_site = get_current_site(request)
            mail_subject = 'Activate your Aura Books account.'
            message = render_to_string('store/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('username') # fallback if no email field in UserCreationForm
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            
            return render(request, 'store/check_email.html', {})
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('store:home')
    else:
        return render(request, 'store/activation_invalid.html', {})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store:home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('store:home')
