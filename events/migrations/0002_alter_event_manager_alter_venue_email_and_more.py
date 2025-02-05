# Generated by Django 4.0.6 on 2022-08-03 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='venue',
            name='email',
            field=models.EmailField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='venue',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Venue Phone'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='web',
            field=models.URLField(blank=True, verbose_name='Venue Web'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='zip',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
