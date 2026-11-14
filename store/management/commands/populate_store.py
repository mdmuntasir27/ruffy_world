from django.core.management.base import BaseCommand
from store.models import Product


class Command(BaseCommand):
    help = 'Populates dummy pet accessories into the Ruffy World store'

    def handle(self, *args, **options):
        accessories = [
            # Cages & Carriers
            {
                'name': 'Heavy-Duty Foldable Dog Cage (36-inch)',
                'category': 'cage',
                'description': 'Sturdy iron wire crate with double-door design and removable leak-proof plastic pan. Easy to fold and transport.',
                'price': '3200.00',
                'quantity': 15,
            },
            {
                'name': 'Portable Airline-Approved Cat & Puppy Carrier',
                'category': 'cage',
                'description': 'Lightweight breathable pet carrier with mesh windows, cozy fleece pad, and secure zipper lock.',
                'price': '1850.00',
                'quantity': 25,
            },
            # Identification Belts & Tags
            {
                'name': 'Reflective Safety Identification Collar Belt',
                'category': 'identification',
                'description': 'Adjustable nylon pet collar with high-visibility reflective stitching, quick-release buckle, and stainless steel ID ring.',
                'price': '350.00',
                'quantity': 60,
            },
            {
                'name': 'Custom Engraved Metal Pet ID Tag',
                'category': 'identification',
                'description': 'Polished alloy paw-shaped tag with space for pet name, owner phone number, and address.',
                'price': '220.00',
                'quantity': 100,
            },
            # Pet Care Books
            {
                'name': 'The Complete Pet Care Handbook & First Aid Guide',
                'category': 'book',
                'description': 'Essential guide covering nutrition, vaccination schedules, grooming tips, and emergency home first aid for cats and dogs.',
                'price': '450.00',
                'quantity': 40,
            },
            {
                'name': 'Positive Reinforcement Puppy Training Manual',
                'category': 'book',
                'description': 'Step-by-step guide to potty training, crate training, leash manners, and socializing your rescue pet.',
                'price': '380.00',
                'quantity': 30,
            },
            # Food & Treats
            {
                'name': 'Royal Canin Maxi Adult Dog Food (3kg)',
                'category': 'food',
                'description': 'Premium dry dog food supporting optimal digestive health, bone and joint integrity, and radiant coat condition.',
                'price': '2400.00',
                'quantity': 35,
            },
            {
                'name': 'Whiskas Ocean Fish Adult Cat Food (1.2kg)',
                'category': 'food',
                'description': 'Complete and balanced nutrition with delicious crunchy pockets, real fish protein, and essential omega fatty acids.',
                'price': '850.00',
                'quantity': 50,
            },
            # Ropes & Leashes
            {
                'name': 'Durable Climbing Rope Pet Leash (5 ft)',
                'category': 'rope',
                'description': 'Braided mountain climbing rope with heavy-duty 360-degree zinc alloy clasp and comfortable padded handle.',
                'price': '480.00',
                'quantity': 45,
            },
            {
                'name': 'Automatic Retractable Dog Leash with Flashlight',
                'category': 'rope',
                'description': 'Tangle-free 5-meter nylon tape leash with one-button brake & lock system and built-in night flashlight.',
                'price': '950.00',
                'quantity': 20,
            },
            # Grooming Brushes
            {
                'name': 'Self-Cleaning Slicker Pet Grooming Brush',
                'category': 'brush',
                'description': 'Gently removes loose fur, tangles, and undercoat. Retractable bristles with push-button fur release.',
                'price': '420.00',
                'quantity': 40,
            },
            {
                'name': 'Double-Sided Pin & Bristle Comb',
                'category': 'brush',
                'description': 'Dual-purpose grooming tool: rounded wire pins for detangling and soft nylon bristles for distributing natural oils.',
                'price': '320.00',
                'quantity': 35,
            },
            # Nail Cutters & Trimmers
            {
                'name': 'Professional Pet Nail Clipper with Quick Guard',
                'category': 'nail_cutter',
                'description': 'Sharp stainless steel blades with safety stop to prevent over-cutting and free hidden mini nail file in handle.',
                'price': '350.00',
                'quantity': 50,
            },
            # Soaps
            {
                'name': 'Natural Neem & Tea Tree Medicated Pet Soap (100g)',
                'category': 'soap',
                'description': 'Herbal anti-bacterial and anti-fungal soap that relieves itching, protects against fleas and ticks, and leaves a fresh scent.',
                'price': '150.00',
                'quantity': 80,
            },
            {
                'name': 'Aloe Vera & Oatmeal Moisturizing Pet Soap',
                'category': 'soap',
                'description': 'Soothing hypoallergenic formula crafted for pets with sensitive, dry, or allergic skin.',
                'price': '180.00',
                'quantity': 75,
            },
            # Shampoos
            {
                'name': 'Ruffy Soft & Shiny Coat Conditioner & Shampoo (400ml)',
                'category': 'shampoo',
                'description': 'Tearless formula enriched with coconut oil and Vitamin E for a silky, knot-free coat.',
                'price': '520.00',
                'quantity': 45,
            },
            {
                'name': 'Anti-Tick & Flea Defense Pet Shampoo (300ml)',
                'category': 'shampoo',
                'description': 'Vet-approved pest control wash that terminates ticks, fleas, and lice on contact while soothing irritated skin.',
                'price': '480.00',
                'quantity': 50,
            },
            # Other Accessories
            {
                'name': 'Stainless Steel Non-Skid Dual Pet Feeding Bowls',
                'category': 'other',
                'description': 'Rust-resistant double feeder bowls set in a silicone non-slip mat to prevent food and water spills.',
                'price': '680.00',
                'quantity': 30,
            },
            {
                'name': 'Interactive Squeaky Chew Toy Set (Pack of 3)',
                'category': 'other',
                'description': 'Non-toxic natural rubber toys designed for teething, boredom relief, and dental plaque cleaning.',
                'price': '390.00',
                'quantity': 60,
            },
            {
                'name': 'Ultra-Absorbent Puppy Training Pee Pads (30 pcs)',
                'category': 'other',
                'description': '5-layer leak-proof training pads with pheromone attractant and odor neutralizing core.',
                'price': '850.00',
                'quantity': 0, # Intentionally set to 0 to demonstrate the "out of stock" functionality!
            },
        ]

        if Product.objects.count() == 0:
            for item in accessories:
                Product.objects.create(**item)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully populated store: {len(accessories)} products created.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                'Store already has products, skipping populate to preserve your changes.'
            ))

