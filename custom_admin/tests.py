from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from pets.models import Pet
from store.models import Product, Order
from vets.models import Vet
from community.models import AdoptionPost, AdoptionInquiry
from adoptions.models import AdoptionRequest


class CustomAdminPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin", password="admin123", email="admin@ruffyworld.com")
        self.user = User.objects.create_user(username="testuser", password="UserPass123!@#", email="user@ruffyworld.com")

        self.pet = Pet.objects.create(
            name="Charlie", animal_type="Dog", breed="Beagle",
            age="1 year 6 months", gender="Male", location="Dhaka",
            price=5000, price_type="fixed", status="Available"
        )
        self.product = Product.objects.create(
            name="Deluxe Dog Cage", category="cage", price=3500, quantity=10
        )
        self.vet = Vet.objects.create(
            name="Rahman", specialization="Surgery", phone="01712345678",
            shift="morning", clinic_address="Dhanmondi, Dhaka", is_available=True
        )

    def test_admin_dashboard_kpis(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse('custom_admin:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Store Pets")
        self.assertContains(response, "Store Accessories")
        self.assertContains(response, "Veterinarians")

    def test_admin_pet_crud(self):
        self.client.login(username="admin", password="admin123")
        # List
        response = self.client.get(reverse('custom_admin:pet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Charlie")

        # Add
        add_response = self.client.post(reverse('custom_admin:pet_add'), {
            'name': 'Bella',
            'animal_type': 'Cat',
            'breed': 'Persian',
            'age': '8 months',
            'gender': 'Female',
            'location': 'Chittagong',
            'price': 4000,
            'price_type': 'fixed',
            'status': 'Available',
            'description': 'Friendly and playful kitten',
        })
        self.assertRedirects(add_response, reverse('custom_admin:pet_list'))
        self.assertTrue(Pet.objects.filter(name='Bella').exists())

        # Edit
        edit_response = self.client.post(reverse('custom_admin:pet_edit', args=[self.pet.pk]), {
            'name': 'Charlie Updated',
            'animal_type': 'Dog',
            'breed': 'Beagle',
            'age': '2 years',
            'gender': 'Male',
            'location': 'Dhaka',
            'price': 5500,
            'price_type': 'fixed',
            'status': 'Available',
        })
        self.assertRedirects(edit_response, reverse('custom_admin:pet_list'))
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.name, 'Charlie Updated')

        # Delete
        del_response = self.client.post(reverse('custom_admin:pet_delete', args=[self.pet.pk]))
        self.assertRedirects(del_response, reverse('custom_admin:pet_list'))
        self.assertFalse(Pet.objects.filter(pk=self.pet.pk).exists())

    def test_admin_product_crud(self):
        self.client.login(username="admin", password="admin123")
        # Add product
        response = self.client.post(reverse('custom_admin:product_add'), {
            'name': 'Organic Pet Shampoo',
            'category': 'shampoo',
            'price': 650,
            'quantity': 25,
            'description': 'Gentle chamomile scent',
        })
        self.assertRedirects(response, reverse('custom_admin:product_list'))
        self.assertTrue(Product.objects.filter(name='Organic Pet Shampoo').exists())

        # Out of stock display
        out_prod = Product.objects.create(name='Zero Stock Collar', category='identification', price=200, quantity=0)
        list_response = self.client.get(reverse('custom_admin:product_list'))
        self.assertContains(list_response, "Out of Stock")

    def test_admin_user_management_no_password_field(self):
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse('custom_admin:user_edit', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        # Verify security policy notice is present
        self.assertContains(response, "Security Policy")
        # Verify password input field is NOT in form
        self.assertNotContains(response, 'type="password"')

    def test_admin_order_list_and_detail(self):
        self.client.login(username="admin", password="admin123")
        order = Order.objects.create(
            user=self.user,
            full_name="Test Customer",
            phone="01712345678",
            shipping_address="Dhanmondi, Dhaka",
            total_amount=3500.00,
            payment_method="cod",
            payment_status="pending",
            status="pending"
        )
        # Test order list rendering with orders
        response = self.client.get(reverse('custom_admin:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"#{order.pk}")
        self.assertContains(response, "Test Customer")

        # Test order detail rendering
        detail_response = self.client.get(reverse('custom_admin:order_detail', args=[order.pk]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, f"Order #{order.pk}")
        self.assertContains(detail_response, "Digital Receipt")
