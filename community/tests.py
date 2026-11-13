from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from community.models import AdoptionPost, AdoptionInquiry


class CommunityFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(username="author", password="AuthorPass123!@#")
        self.requester = User.objects.create_user(username="requester", password="ReqPass123!@#")
        self.post = AdoptionPost.objects.create(
            author=self.author,
            pet_name="Kitten Milo",
            animal_type="Cat",
            breed="Local Mix",
            age="3 months",
            gender="Male",
            location="Dhanmondi, Dhaka",
            description="Playful and sweet kitten needing a loving home.",
            status="Open",
        )

    def test_community_age_text_field(self):
        self.assertEqual(self.post.age, "3 months")

    def test_inquiry_status_approved_available(self):
        inquiry = AdoptionInquiry.objects.create(
            post=self.post,
            requester=self.requester,
            message="We would love to adopt Milo!",
            contact_phone="01711223344",
            contact_address="House 10, Road 2, Dhanmondi",
            status="Approved",
        )
        self.assertEqual(inquiry.status, "Approved")
        self.assertIn(('Approved', 'Approved'), AdoptionInquiry.STATUS_CHOICES)

    def test_update_inquiry_status_view_approved(self):
        inquiry = AdoptionInquiry.objects.create(
            post=self.post,
            requester=self.requester,
            message="Looking for a pet",
            contact_phone="01711223344",
            contact_address="Dhaka",
            status="Pending",
        )
        self.client.login(username="author", password="AuthorPass123!@#")
        response = self.client.post(
            reverse('update_inquiry_status', kwargs={'inquiry_pk': inquiry.pk}),
            {'status': 'Approved'}
        )
        self.assertEqual(response.status_code, 302)
        inquiry.refresh_from_db()
        self.assertEqual(inquiry.status, "Approved")
