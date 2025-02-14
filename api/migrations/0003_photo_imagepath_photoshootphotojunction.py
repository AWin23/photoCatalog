# Generated by Django 4.2.16 on 2025-02-14 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_photoshoot_locationid'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='ImagePath',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.CreateModel(
            name='PhotoshootPhotoJunction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PhotoID', models.ForeignKey(db_column='PhotoID', on_delete=django.db.models.deletion.CASCADE, to='api.photo')),
                ('PhotoshootId', models.ForeignKey(db_column='PhotoshootID', on_delete=django.db.models.deletion.CASCADE, to='api.photoshoot')),
            ],
            options={
                'db_table': 'PhotoshootPhotoJunction',
            },
        ),
    ]
