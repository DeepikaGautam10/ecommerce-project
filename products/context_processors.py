from .models import CartItem


def cart_count(request):
    """Expose the number of items in the logged-in user's cart to all templates."""
    count = 0
    if request.user.is_authenticated:
        count = (
            CartItem.objects
            .filter(cart__user=request.user)
            .count()
        )
    return {'cart_count': count}
