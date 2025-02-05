# Generated by Django 4.0.6 on 2022-08-26 17:42

from django.db import migrations
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0036_alter_venue_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['event_date', django.db.models.functions.text.Upper('venue')]},
        ),
        migrations.AlterModelOptions(
            name='venue',
            options={'ordering': [django.db.models.functions.text.Upper('name'), django.db.models.functions.text.Upper('city')]},
        ),
    ]
