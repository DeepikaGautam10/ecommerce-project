from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from .models import Product, Category, Cart, CartItem
from .forms import ProductForm, CategoryForm

PRODUCTS_PER_PAGE = 9


# ----------------------------------------------------------------------
# Public storefront
# ----------------------------------------------------------------------
HERO_PRODUCT_SLUG = 'tissot-prx-powermatic-80'


def home_view(request):
    """Landing page: hero feature + product carousel, latest arrivals, categories."""
    featured = Product.objects.filter(featured=True).select_related('category')

    # Spotlight one watch in the hero; fall back to the newest featured item.
    hero_product = (
        featured.filter(slug=HERO_PRODUCT_SLUG).first()
        or featured.exclude(image='').first()
    )

    # Keep the hero out of the trending carousel so it is not shown twice.
    carousel = featured.exclude(pk=hero_product.pk) if hero_product else featured

    context = {
        'hero_product': hero_product,
        'featured_products': carousel[:8],
        'latest_products': Product.objects.select_related('category')[:8],
        'categories': Category.objects.all()[:6],
    }
    return render(request, 'products/home.html', context)


def shop_view(request):
    """Product catalogue with category filter, search and pagination."""
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()

    current_category = None
    if category_slug:
        current_category = categories.filter(slug=category_slug).first()
        products = products.filter(category__slug=category_slug)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'total_count': paginator.count,
        'categories': categories,
        'current_category': category_slug,
        'current_category_obj': current_category,
        'search_query': search_query,
    }
    return render(request, 'products/shop.html', context)


def product_detail_view(request, slug):
    """Single product page with related items from the same category."""
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)
    related_products = (
        Product.objects
        .filter(category=product.category)
        .exclude(id=product.id)[:4]
    )
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


# ----------------------------------------------------------------------
# Shopping cart
# ----------------------------------------------------------------------
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'products/cart.html', {'cart': cart})


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add one unit of a product to the cart, respecting available stock."""
    product = get_object_or_404(Product, id=product_id)

    if product.stock < 1:
        messages.error(request, f'"{product.name}" is currently out of stock.')
        return redirect('products:product_detail', slug=product.slug)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        if cart_item.quantity + 1 > product.stock:
            messages.warning(request, f'Only {product.stock} unit(s) of "{product.name}" available.')
            return redirect('products:cart')
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'"{product.name}" added to your cart.')
    return redirect('products:cart')


@login_required
@require_POST
def update_cart(request, item_id):
    """Update the quantity of a cart item, or remove it when set to zero."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    elif quantity > cart_item.product.stock:
        cart_item.quantity = cart_item.product.stock
        cart_item.save()
        messages.warning(request, f'Quantity limited to {cart_item.product.stock} (available stock).')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')

    return redirect('products:cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'"{product_name}" removed from cart.')
    return redirect('products:cart')


# ----------------------------------------------------------------------
# Admin - Category management
# ----------------------------------------------------------------------
@login_required
@role_required(['admin'])
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})


@login_required
@role_required(['admin'])
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('products:category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form, 'action': 'Create'})


@login_required
@role_required(['admin'])
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form, 'action': 'Update'})


@login_required
@role_required(['admin'])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('products:category_list')
    return render(request, 'products/category_confirm_delete.html', {'category': category})


# ----------------------------------------------------------------------
# Admin - Product management
# ----------------------------------------------------------------------
@login_required
@role_required(['admin'])
def product_list_admin(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'products/product_list_admin.html', {'products': products})


@login_required
@role_required(['admin'])
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('products:product_list_admin')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Create'})


@login_required
@role_required(['admin'])
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products:product_list_admin')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Update'})


@login_required
@role_required(['admin'])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('products:product_list_admin')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
