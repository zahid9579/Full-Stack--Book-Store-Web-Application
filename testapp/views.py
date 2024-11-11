from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Cart, CartItem, Category
from .forms import BookForm, UserRegistrationForm, DeliveryInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index_views(request):
    return render(request, 'index.html')

# Book List View
def book_list_view(request):
    technical_category = Category.objects.get(name="Technical")
    motivational_category = Category.objects.get(name="Motivational")

    technical_books = Book.objects.filter(category=technical_category)
    motivational_books = Book.objects.filter(category=motivational_category)

    return render(request, 'book_list.html', {
        'technical_books': technical_books,
        'motivational_books': motivational_books,
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Fetch ordered books for the current user
    ordered_books = CartItem.objects.filter(cart__user=request.user).values_list('book_id', flat=True)
    
    context = {
        'book': book,
        'ordered_books': ordered_books,
    }
    return render(request, 'book_detail.html', context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Get or create the cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get the count of items in the cart using 'items' related_name
    cart_items_count = cart.items.count()  # Access the related items with 'items'
    
    # Add the book to the cart (or increase quantity if already in the cart)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Update cart items count after adding/updating item
    cart_items_count = cart.items.count()  # Recount items after adding/updating

    # Pass the cart count to the template
    context = {
        'book': book,
        'cart_items_count': cart_items_count,
    }
    return render(request, 'book_detail.html', context)

    
    
# Order Now View
@login_required
def order_now(request, book_id):
    book = get_object_or_404(Book, id=book_id)  # Get the book instance

    if request.method == 'POST':
        # Handle form submission for delivery info
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            delivery_info = form.save(commit=False)  # Do not save yet
            delivery_info.user = request.user  # Associate with the current user
            delivery_info.save()  # Save the delivery info

            # Create or get the user's cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

            if created:
                cart_item.quantity = 1  # New item, set initial quantity
            else:
                cart_item.quantity += 1  # Increment quantity if it already exists
            
            cart_item.save()

            # Add a success message after placing the order
            messages.success(request, "Order placed successfully!")
            return redirect('book_detail', book_id=book.id) # Redirect to a success page after saving the order
            
    else:
        form = DeliveryInfoForm()  # Create a new form instance

    return render(request, 'delivery_info.html', {'form': form, 'book': book})


# Cancel Item View
@login_required
def cancel_item(request, book_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, book__id=book_id)
    
    cart_item.delete()  # Remove the item from the cart
    
    # Add a success message after cancellation
    messages.success(request, "Order cancelled successfully.")
    return redirect('book_detail', book_id=book_id)

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
