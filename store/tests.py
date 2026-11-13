from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from store.models import Product, Order, OrderItem


class StoreEcommerceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="shopper", password="ShopperPass123!@#")
        self.product = Product.objects.create(
            name="Large Dog Cage",
            category="cage",
            description="Sturdy iron cage",
            price=2500.00,
            quantity=3,
        )

    def test_product_in_stock_and_out_of_stock_property(self):
        self.assertTrue(self.product.is_in_stock)
        self.product.quantity = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock)

    def test_add_to_cart_and_view_cart(self):
        response = self.client.post(reverse('add_to_cart', kwargs={'pk': self.product.pk}), {'quantity': 2})
        self.assertEqual(response.status_code, 302)
        cart_resp = self.client.get(reverse('view_cart'))
        self.assertEqual(cart_resp.status_code, 200)
        self.assertContains(cart_resp, "Large Dog Cage")
        self.assertContains(cart_resp, "BDT 5000.0")

    def test_checkout_decrements_stock_and_creates_order_cod(self):
        self.client.login(username="shopper", password="ShopperPass123!@#")
        # Add to cart
        self.client.post(reverse('add_to_cart', kwargs={'pk': self.product.pk}), {'quantity': 2})
        # Checkout
        checkout_data = {
            'full_name': 'Shopper Person',
            'phone': '01700000000',
            'shipping_address': 'House 1, Road 2, Dhaka',
            'payment_method': 'cod',
        }
        response = self.client.post(reverse('checkout'), checkout_data)
        self.assertEqual(response.status_code, 302)

        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.payment_method, 'cod')
        self.assertEqual(order.payment_status, 'pending')
        self.assertEqual(float(order.total_amount), 5000.00)

        # Verify stock was decremented from 3 to 1
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 1)

    def test_checkout_online_payment_marks_paid(self):
        self.client.login(username="shopper", password="ShopperPass123!@#")
        self.client.post(reverse('add_to_cart', kwargs={'pk': self.product.pk}), {'quantity': 1})
        checkout_data = {
            'full_name': 'Shopper Person',
            'phone': '01700000000',
            'shipping_address': 'House 1, Road 2, Dhaka',
            'payment_method': 'online',
        }
        response = self.client.post(reverse('checkout'), checkout_data)
        self.assertEqual(response.status_code, 302)

        order = Order.objects.filter(user=self.user).latest('id')
        self.assertEqual(order.payment_method, 'online')
        self.assertEqual(order.payment_status, 'paid')

    def test_digital_receipt_view(self):
        self.client.login(username="shopper", password="ShopperPass123!@#")
        order = Order.objects.create(
            user=self.user,
            full_name="Receipt User",
            phone="01712345678",
            shipping_address="Banani, Dhaka",
            payment_method="online",
            payment_status="paid",
            total_amount=2500.00
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name=self.product.name,
            quantity=1,
            price_at_purchase=2500.00
        )
        response = self.client.get(reverse('download_receipt', kwargs={'pk': order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Official Digital Receipt")
        self.assertContains(response, "Online Payment")
        self.assertContains(response, "PAID IN FULL")

