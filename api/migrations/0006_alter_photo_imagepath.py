# Generated by Django 4.2.16 on 2025-02-14 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_photo_imagepath'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='ImagePath',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
