from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='age',
            field=models.CharField(blank=True, default='', help_text='e.g. 2 years 3 months', max_length=50),
        ),
    ]
