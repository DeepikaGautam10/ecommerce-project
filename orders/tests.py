from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from products.models import Category, Product, Cart, CartItem
from .models import Order


class CheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('buyer', 'buyer@x.com', 'pw12345!')
        category = Category.objects.create(name='Classic', slug='classic')
        self.product = Product.objects.create(
            name='Seiko 5', slug='seiko-5', description='Automatic watch.',
            price=Decimal('200.00'), stock=10, category=category,
        )
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.client.login(username='buyer', password='pw12345!')

    def test_checkout_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 302)

    def test_checkout_creates_order_and_clears_cart(self):
        response = self.client.post(reverse('orders:checkout'), {
            'full_name': 'Test Buyer',
            'email': 'buyer@x.com',
            'phone': '9800000000',
            'shipping_address': '123 Street',
            'city': 'Kathmandu',
            'postal_code': '44600',
            'payment_method': 'cash_on_delivery',
            'notes': '',
        })
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_amount, Decimal('400.00'))
        self.assertEqual(Cart.objects.get(user=self.user).items.count(), 0)

    def test_checkout_reduces_product_stock(self):
        self.client.post(reverse('orders:checkout'), {
            'full_name': 'Test Buyer',
            'email': 'buyer@x.com',
            'phone': '9800000000',
            'shipping_address': '123 Street',
            'city': 'Kathmandu',
            'payment_method': 'cash_on_delivery',
        })
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)  # 10 - 2

    def test_checkout_with_missing_fields_does_not_create_order(self):
        self.client.post(reverse('orders:checkout'), {'full_name': 'Test Buyer'})
        self.assertFalse(Order.objects.filter(user=self.user).exists())


class ManageOrderTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user('cust', 'cust@x.com', 'pw12345!')
        self.staff = User.objects.create_user('staff', 'staff@x.com', 'pw12345!', is_staff=True)
        category = Category.objects.create(name='Digital', slug='digital')
        product = Product.objects.create(
            name='Casio F-91W', slug='casio-f91w', description='Digital watch.',
            price=Decimal('100.00'), stock=10, category=category,
        )
        self.order = Order.objects.create(
            user=self.customer, full_name='Cust', email='cust@x.com', phone='980',
            shipping_address='1 St', city='KTM', payment_method='cash_on_delivery',
            total_amount=Decimal('100.00'),
        )

    def test_manage_dashboard_requires_staff(self):
        self.client.login(username='cust', password='pw12345!')
        response = self.client.get(reverse('orders:manage_order_list'))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_view_manage_dashboard(self):
        self.client.login(username='staff', password='pw12345!')
        response = self.client.get(reverse('orders:manage_order_list'))
        self.assertContains(response, f'Order #{self.order.id}')

    def test_staff_can_update_order_status(self):
        self.client.login(username='staff', password='pw12345!')
        self.client.post(
            reverse('orders:manage_order_update_status', args=[self.order.id]),
            {'status': 'delivered'},
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'delivered')

    def test_invalid_status_is_rejected(self):
        self.client.login(username='staff', password='pw12345!')
        self.client.post(
            reverse('orders:manage_order_update_status', args=[self.order.id]),
            {'status': 'not-a-status'},
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'pending')
