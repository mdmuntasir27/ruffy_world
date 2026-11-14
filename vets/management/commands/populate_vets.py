from django.core.management.base import BaseCommand
from vets.models import Vet


class Command(BaseCommand):
    help = 'Populates dummy veterinarians across 3 8-hour shifts'

    def handle(self, *args, **options):
        vets = [
            # Morning Shift: 6:00 AM – 2:00 PM (2 Vets)
            {
                'name': 'Ayesha Rahman',
                'specialization': 'Small Animal Surgery & General Practitioner',
                'phone': '+880 1711-234567',
                'email': 'dr.ayesha@ruffyworld.com',
                'clinic_address': 'Dhanmondi Pet Clinic, House 24, Road 4, Dhanmondi, Dhaka',
                'shift': 'morning',
                'is_available': True,
                'bio': 'DVM, MS in Veterinary Surgery with over 9 years of experience in feline and canine clinical medicine.',
            },
            {
                'name': 'Tanvir Hossain',
                'specialization': 'Avian Medicine, Rabbits & Exotic Companion Pets',
                'phone': '+880 1812-345678',
                'email': 'dr.tanvir@ruffyworld.com',
                'clinic_address': 'CarePaws Hospital, Plot 15, Sector 7, Uttara, Dhaka',
                'shift': 'morning',
                'is_available': True,
                'bio': 'Certified specialist in birds, parrots, rabbits, and small mammals. Expert in gentle diagnostic handling.',
            },

            # Mid Shift: 2:00 PM – 10:00 PM (2 Vets)
            {
                'name': 'Sadia Chowdhury',
                'specialization': 'Veterinary Dermatology, Allergies & Nutrition',
                'phone': '+880 1913-456789',
                'email': 'dr.sadia@ruffyworld.com',
                'clinic_address': 'Gulshan Animal Health Centre, Block D, Road 11, Banani, Dhaka',
                'shift': 'mid',
                'is_available': True,
                'bio': 'Specialized in treating chronic pet dermatological conditions, fungal infections, food allergies, and diet planning.',
            },
            {
                'name': 'Tariqul Islam',
                'specialization': 'Canine Orthopedics, Joint Care & Physical Rehabilitation',
                'phone': '+880 1614-567890',
                'email': 'dr.tariqul@ruffyworld.com',
                'clinic_address': 'Mirpur Pet Hospital, Section 10, Mirpur, Dhaka',
                'shift': 'mid',
                'is_available': True,
                'bio': 'Orthopedic surgeon focusing on joint dysplasia, fracture fixations, and geriatric mobility care for older dogs.',
            },

            # Night Shift: 10:00 PM – 6:00 AM (2 Vets)
            {
                'name': 'Farhana Akter',
                'specialization': 'Emergency Trauma, Toxic Exposure & Critical Care',
                'phone': '+880 1515-678901',
                'email': 'dr.farhana@ruffyworld.com',
                'clinic_address': '24/7 Central Emergency Animal Hospital, Green Road, Farmgate, Dhaka',
                'shift': 'night',
                'is_available': True,
                'bio': 'Dedicated night emergency physician handling acute poisoning, respiratory distress, shock treatment, and sudden trauma.',
            },
            {
                'name': 'Mahbubur Rahman',
                'specialization': 'Emergency Internal Medicine & Urgent Surgical Care',
                'phone': '+880 1316-789012',
                'email': 'dr.mahbubur@ruffyworld.com',
                'clinic_address': 'Panthapath Pet ICU, 42 Panthapath, Dhaka',
                'shift': 'night',
                'is_available': True,
                'bio': 'Over 8 years of overnight ICU emergency supervision with on-site blood gas analysis and emergency ultrasound capability.',
            },
        ]

        if Vet.objects.count() == 0:
            for item in vets:
                Vet.objects.create(**item)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully populated vets: {len(vets)} veterinarians created.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                'Veterinarians directory already populated, skipping to preserve your changes.'
            ))

