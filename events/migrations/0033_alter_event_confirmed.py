# Generated by Django 4.0.6 on 2022-08-23 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0032_event_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='confirmed',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', max_length=5, verbose_name='Confirmation'),
        ),
    ]
