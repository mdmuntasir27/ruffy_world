from django.db import migrations, models


def contacted_to_approved(apps, schema_editor):
    AdoptionInquiry = apps.get_model('community', 'AdoptionInquiry')
    AdoptionInquiry.objects.filter(status='Contacted').update(status='Approved')


def approved_to_contacted(apps, schema_editor):
    AdoptionInquiry = apps.get_model('community', 'AdoptionInquiry')
    AdoptionInquiry.objects.filter(status='Approved').update(status='Contacted')


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_alter_adoptionpost_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptioninquiry',
            name='status',
            field=models.CharField(
                choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
                default='Pending',
                max_length=20,
            ),
        ),
        migrations.RunPython(contacted_to_approved, approved_to_contacted),
    ]
