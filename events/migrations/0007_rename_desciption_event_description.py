# Generated by Django 4.0.6 on 2022-08-05 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_venue_province'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='desciption',
            new_name='description',
        ),
    ]
