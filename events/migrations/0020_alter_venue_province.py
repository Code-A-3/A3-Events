# Generated by Django 4.0.6 on 2022-08-13 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_alter_venue_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='province',
            field=models.CharField(max_length=20, verbose_name='Venue Province'),
        ),
    ]
