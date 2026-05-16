from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Category, Product, Cart, CartItem


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Luxury', slug='luxury')
        self.product = Product.objects.create(
            name='Rolex', slug='rolex', description='A watch.',
            price=Decimal('100.00'), stock=5, category=self.category,
        )

    def test_is_in_stock_true_when_stock_positive(self):
        self.assertTrue(self.product.is_in_stock)

    def test_is_in_stock_false_when_stock_zero(self):
        self.product.stock = 0
        self.assertFalse(self.product.is_in_stock)

    def test_cart_item_subtotal(self):
        cart = Cart.objects.create(user=User.objects.create_user('u1', 'u1@x.com', 'pw'))
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=3)
        self.assertEqual(item.subtotal, Decimal('300.00'))

    def test_cart_total_price(self):
        cart = Cart.objects.create(user=User.objects.create_user('u2', 'u2@x.com', 'pw'))
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.total_price, Decimal('200.00'))


class StorefrontViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Sports', slug='sports')
        self.product = Product.objects.create(
            name='Casio', slug='casio', description='Digital watch.',
            price=Decimal('50.00'), stock=10, category=self.category,
        )

    def test_home_page_loads(self):
        self.assertEqual(self.client.get(reverse('products:home')).status_code, 200)

    def test_shop_page_loads(self):
        self.assertEqual(self.client.get(reverse('products:shop')).status_code, 200)

    def test_shop_search_finds_product(self):
        response = self.client.get(reverse('products:shop'), {'q': 'Casio'})
        self.assertContains(response, 'Casio')

    def test_product_detail_loads(self):
        url = reverse('products:product_detail', args=[self.product.slug])
        self.assertContains(self.client.get(url), 'Casio')


class CartViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('shopper', 'shopper@x.com', 'pw12345!')
        self.category = Category.objects.create(name='Smart', slug='smart')
        self.product = Product.objects.create(
            name='Apple Watch', slug='apple-watch', description='Smart watch.',
            price=Decimal('400.00'), stock=3, category=self.category,
        )

    def test_cart_requires_login(self):
        response = self.client.get(reverse('products:cart'))
        self.assertEqual(response.status_code, 302)

    def test_add_to_cart_creates_item(self):
        self.client.login(username='shopper', password='pw12345!')
        self.client.post(reverse('products:add_to_cart', args=[self.product.id]))
        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 1)

    def test_add_to_cart_does_not_exceed_stock(self):
        self.client.login(username='shopper', password='pw12345!')
        url = reverse('products:add_to_cart', args=[self.product.id])
        for _ in range(6):  # stock is only 3
            self.client.post(url)
        item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertLessEqual(item.quantity, self.product.stock)
