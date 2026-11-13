from django.db import models


class Vet(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Morning Shift (6:00 AM – 2:00 PM)'),
        ('mid', 'Mid Shift (2:00 PM – 10:00 PM)'),
        ('night', 'Night Shift (10:00 PM – 6:00 AM)'),
    ]

    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=200, help_text='e.g. Small Animal Surgery & General Medicine')
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    clinic_address = models.CharField(max_length=250, help_text='Clinic name and address')
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    is_available = models.BooleanField(default=True, help_text='Is this vet currently active and practicing?')
    bio = models.TextField(blank=True, help_text='Short description, degrees, and qualifications')
    image = models.ImageField(upload_to='vets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['shift', 'name']

    def __str__(self):
        return f'Dr. {self.name} ({self.get_shift_display()})'

    @property
    def shift_time_range(self):
        ranges = {
            'morning': '6:00 AM – 2:00 PM',
            'mid': '2:00 PM – 10:00 PM',
            'night': '10:00 PM – 6:00 AM',
        }
        return ranges.get(self.shift, '')

