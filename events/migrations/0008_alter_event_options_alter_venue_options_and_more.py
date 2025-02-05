# Generated by Django 4.0.6 on 2022-08-10 13:10

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_rename_desciption_event_description'),
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
        migrations.AlterField(
            model_name='webuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='nick',
            field=models.CharField(max_length=20, unique=True, verbose_name='User Nick'),
        ),
    ]
