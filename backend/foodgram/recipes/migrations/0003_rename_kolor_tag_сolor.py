# Generated by Django 3.2.16 on 2023-03-04 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rename_сolor_tag_kolor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='kolor',
            new_name='сolor',
        ),
    ]
