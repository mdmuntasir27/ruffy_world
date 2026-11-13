from django.test import TestCase, Client
from django.urls import reverse
from pets.models import Pet


class PetModelAndFilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.pet_avail = Pet.objects.create(
            name="Charlie",
            animal_type="Dog",
            breed="Labrador",
            age="2 years 3 months",
            gender="Male",
            location="Dhaka",
            description="Friendly dog",
            price=2500.00,
            price_type="negotiable",
            status="Available",
        )
        self.pet_adopted = Pet.objects.create(
            name="Luna",
            animal_type="Cat",
            breed="Persian",
            age="1 year",
            gender="Female",
            location="Chittagong",
            description="Calm cat",
            price=3000.00,
            price_type="fixed",
            status="Adopted",
        )

    def test_age_as_text(self):
        pet = Pet.objects.get(name="Charlie")
        self.assertEqual(pet.age, "2 years 3 months")

    def test_price_and_price_type(self):
        pet = Pet.objects.get(name="Charlie")
        self.assertEqual(float(pet.price), 2500.00)
        self.assertEqual(pet.price_type, "negotiable")

    def test_default_filter_shows_available_only(self):
        response = self.client.get(reverse('pet_list'))
        self.assertEqual(response.status_code, 200)
        object_list = response.context['page_obj'].object_list
        self.assertIn(self.pet_avail, object_list)
        self.assertNotIn(self.pet_adopted, object_list)

    def test_filter_all_shows_both(self):
        response = self.client.get(reverse('pet_list'), {'status': 'all'})
        self.assertEqual(response.status_code, 200)
        object_list = response.context['page_obj'].object_list
        self.assertIn(self.pet_avail, object_list)
        self.assertIn(self.pet_adopted, object_list)
