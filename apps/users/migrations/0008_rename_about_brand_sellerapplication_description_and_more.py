# Generated by Django 5.1.6 on 2025-03-31 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_sellerapplication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sellerapplication',
            old_name='about_brand',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='sellerapplication',
            name='contact_name',
        ),
        migrations.RemoveField(
            model_name='sellerapplication',
            name='phone_number',
        ),
    ]
