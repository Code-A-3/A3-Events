# Generated by Django 4.0.6 on 2022-08-12 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_event_manager_alter_event_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
