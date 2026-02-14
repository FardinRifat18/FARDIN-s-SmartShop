# core/context_processors.py
from .models import Cart, CartItem
from django.conf import settings

def cart_count(request):
    """
    Returns the number of items in the cart for the current user/session
    """
    CART_SESSION_ID = getattr(settings, 'CART_SESSION_ID', 'cart')
    
    # Authenticated user - get from database
    if request.user.is_authenticated:
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            count = sum(item.quantity for item in cart.items.all())
        except Exception:
            count = 0
    else:
        # Anonymous user - get from session
        cart = request.session.get(CART_SESSION_ID, {})
        count = sum(item.get('quantity', 0) for item in cart.values())
    
    return {'cart_count': count}
