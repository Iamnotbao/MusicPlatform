# Generated by Django 4.2.4 on 2023-11-08 13:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('musicPlatform', '0007_remove_music_artwork_review_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='create_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
