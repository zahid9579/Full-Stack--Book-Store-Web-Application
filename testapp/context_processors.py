from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        # Use the custom related name 'items'
        cart_items_count = cart.items.count() if cart else 0  # Changed this line
    else:
        cart_items_count = 0
    return {'cart_items_count': cart_items_count}
