# Generated by Django 5.0.4 on 2024-04-24 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CarDekho_app', '0007_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='updared_at',
            new_name='updated_at',
        ),
    ]
