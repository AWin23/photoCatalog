# Generated by Django 4.2.16 on 2024-12-04 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_photo_photoguid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='PhotoGUID',
        ),
    ]
