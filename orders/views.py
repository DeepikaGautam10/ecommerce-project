from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from products.models import Cart
from .models import Order, OrderItem


@login_required
def checkout_view(request):
    """Collect shipping details and convert the cart into an order."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('products:cart')

    if request.method == 'POST':
        # Validate stock before taking payment / creating the order
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(
                    request,
                    f'Not enough stock for "{item.product.name}". '
                    f'Only {item.product.stock} available.'
                )
                return redirect('products:cart')

        required = ['full_name', 'email', 'phone', 'shipping_address', 'city', 'payment_method']
        if not all(request.POST.get(field, '').strip() for field in required):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'orders/checkout.html', {'cart': cart, 'form_data': request.POST})

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                full_name=request.POST.get('full_name').strip(),
                email=request.POST.get('email').strip(),
                phone=request.POST.get('phone').strip(),
                shipping_address=request.POST.get('shipping_address').strip(),
                city=request.POST.get('city').strip(),
                postal_code=request.POST.get('postal_code', '').strip(),
                payment_method=request.POST.get('payment_method'),
                total_amount=cart.total_price,
                notes=request.POST.get('notes', '').strip(),
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                # Reduce product stock
                item.product.stock -= item.quantity
                item.product.save()

            # Empty the cart
            cart.items.all().delete()

        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user,
    )
    return render(request, 'orders/order_detail.html', {'order': order})


# ----------------------------------------------------------------------
# Staff - Order management
# ----------------------------------------------------------------------
@login_required
@role_required(['admin'])
def manage_order_list(request):
    """Staff dashboard listing every customer order, with an optional
    status filter. Lets the business owner track and fulfil orders."""
    orders = (
        Order.objects
        .select_related('user')
        .prefetch_related('items__product')
    )

    current_status = request.GET.get('status', '')
    if current_status:
        orders = orders.filter(status=current_status)

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': current_status,
    }
    return render(request, 'orders/manage_order_list.html', context)


@login_required
@role_required(['admin'])
@require_POST
def manage_order_update_status(request, order_id):
    """Update the status of a single order (Pending, Processing,
    Shipped, Delivered, Cancelled)."""
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    valid_statuses = dict(Order.STATUS_CHOICES)

    if new_status in valid_statuses:
        order.status = new_status
        order.save()
        messages.success(
            request,
            f'Order #{order.id} updated to "{valid_statuses[new_status]}".'
        )
    else:
        messages.error(request, 'Invalid order status.')

    return redirect('orders:manage_order_list')
