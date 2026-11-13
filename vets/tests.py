from django.test import TestCase, Client
from django.urls import reverse
from vets.models import Vet


class VetDirectoryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.v_morning = Vet.objects.create(
            name="Ayesha Rahman",
            specialization="Surgeon",
            phone="01711234567",
            clinic_address="Dhaka",
            shift="morning",
            is_available=True
        )
        self.v_mid = Vet.objects.create(
            name="Sadia Chowdhury",
            specialization="Dermatologist",
            phone="01913456789",
            clinic_address="Dhaka",
            shift="mid",
            is_available=True
        )
        self.v_night = Vet.objects.create(
            name="Farhana Akter",
            specialization="Emergency",
            phone="01515678901",
            clinic_address="Dhaka",
            shift="night",
            is_available=True
        )

    def test_vet_list_view_loads(self):
        response = self.client.get(reverse('vet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Ayesha Rahman")
        self.assertContains(response, "Dr. Sadia Chowdhury")
        self.assertContains(response, "Dr. Farhana Akter")

    def test_vet_shift_filtering(self):
        response_morning = self.client.get(reverse('vet_list'), {'shift': 'morning'})
        self.assertContains(response_morning, "Dr. Ayesha Rahman")
        self.assertNotContains(response_morning, "Dr. Sadia Chowdhury")

        response_night = self.client.get(reverse('vet_list'), {'shift': 'night'})
        self.assertContains(response_night, "Dr. Farhana Akter")
        self.assertNotContains(response_night, "Dr. Ayesha Rahman")

