# Generated by Django 4.2.4 on 2023-08-15 06:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('musicPlatform', '0005_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
