# Generated by Django 5.1.1 on 2024-09-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0003_alter_phone_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
