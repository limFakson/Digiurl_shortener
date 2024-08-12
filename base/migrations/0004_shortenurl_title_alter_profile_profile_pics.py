# Generated by Django 5.0.7 on 2024-08-12 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_profile_profile_pics'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortenurl',
            name='title',
            field=models.CharField(default='Digicore shortened url', max_length=800),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pics',
            field=models.URLField(default='image/Solo-Leveling-Sung-jin-woo.jpg'),
        ),
    ]