# Generated by Django 3.2.16 on 2023-03-07 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='color',
            new_name='kolor',
        ),
    ]
