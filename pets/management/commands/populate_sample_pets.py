from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pets.models import Pet
from community.models import AdoptionPost


class Command(BaseCommand):
    help = 'Seeds initial sample pets, community posts, and ensures the default admin superuser exists'

    def handle(self, *args, **options):
        # 1. Ensure admin superuser exists
        admin_user, created = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@ruffyworld.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        })
        if created or not admin_user.check_password('admin123'):
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' with password 'admin123' ready."))

        # 2. Seed Foundation Pets if none exist
        if Pet.objects.count() == 0:
            sample_pets = [
                {
                    'name': 'Simba',
                    'animal_type': 'Dog',
                    'breed': 'Bull Dog',
                    'age': '3 years',
                    'gender': 'Male',
                    'location': 'Shaifur er basha, Dhaka',
                    'price': 3500.00,
                    'price_type': 'negotiable',
                    'status': 'Available',
                    'description': "A brave, gentle bulldog trained for house companionship and guarding.",
                },
                {
                    'name': 'Mohammad Sumbul',
                    'animal_type': 'Cat',
                    'breed': 'Local Short Hair',
                    'age': '8 months',
                    'gender': 'Male',
                    'location': 'Merul Badda, Dhaka',
                    'price': 2000.00,
                    'price_type': 'fixed',
                    'status': 'Available',
                    'description': "Rescued and safe at Ruffy World. An energetic, affectionate orange cat looking for a forever loving family.",
                },
                {
                    'name': 'Husk',
                    'animal_type': 'Dog',
                    'breed': 'Husky',
                    'age': '4 years 6 months',
                    'gender': 'Female',
                    'location': 'Rahat er basha, Dhaka',
                    'price': 5000.00,
                    'price_type': 'fixed',
                    'status': 'Available',
                    'description': "Graceful Siberian Husky with beautiful blue eyes. Loves walks, active play, and outdoor runs.",
                },
                {
                    'name': 'Mithu',
                    'animal_type': 'Bird',
                    'breed': 'Parrot',
                    'age': '1 year',
                    'gender': 'Male',
                    'location': 'Mirpur 1, Dhaka',
                    'price': 1200.00,
                    'price_type': 'fixed',
                    'status': 'Available',
                    'description': "Healthy green ringneck parrot, whistle friendly, eats fruits and seeds happily.",
                },
                {
                    'name': 'Chiku',
                    'animal_type': 'Bird',
                    'breed': 'Cockatiel',
                    'age': '2 years 3 months',
                    'gender': 'Female',
                    'location': 'Uttara, Dhaka',
                    'price': 2800.00,
                    'price_type': 'negotiable',
                    'status': 'Adopted',
                    'description': "Tamed cockatiel with sunny yellow crest. Already found a happy home.",
                },
                {
                    'name': 'Ezio Auditore da Firenze',
                    'animal_type': 'Cat',
                    'breed': 'Mixed Persian',
                    'age': '2 years 4 months',
                    'gender': 'Male',
                    'location': 'Uttara, Dhaka',
                    'price': 4500.00,
                    'price_type': 'negotiable',
                    'status': 'Adopted',
                    'description': "Curious cat found exploring rooftop gardens. Very loving and purr-filled.",
                },
                {
                    'name': 'Pimpi',
                    'animal_type': 'Cat',
                    'breed': 'Local Calico',
                    'age': '1 year 2 months',
                    'gender': 'Female',
                    'location': 'Uttara, Dhaka',
                    'price': 1500.00,
                    'price_type': 'fixed',
                    'status': 'Adopted',
                    'description': "Calico cat with calm nature, loves sunny nap spots.",
                },
            ]
            for p_data in sample_pets:
                Pet.objects.create(**p_data)
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(sample_pets)} foundation pets."))

        # 3. Seed sample community post if none exist
        if AdoptionPost.objects.count() == 0:
            AdoptionPost.objects.create(
                author=admin_user,
                pet_name='Snowy',
                animal_type='Rabbit',
                breed='Netherland Dwarf',
                age='6 months',
                gender='Female',
                location='Banani, Dhaka',
                description='Very gentle white dwarf rabbit. Loves carrots, fresh timothy hay, and hopping around safe indoor spaces.',
                status='Open',
            )
            self.stdout.write(self.style.SUCCESS("Seeded sample community adoption post."))
