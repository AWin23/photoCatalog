# Generated by Django 4.2.16 on 2025-02-21 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_location_address_remove_location_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='Address',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='Longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
