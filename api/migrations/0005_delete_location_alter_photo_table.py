# Generated by Django 4.2.16 on 2024-12-04 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_location_alter_photo_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.AlterModelTable(
            name='photo',
            table='Photo',
        ),
    ]
