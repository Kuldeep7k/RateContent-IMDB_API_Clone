# Generated by Django 5.0.6 on 2024-06-10 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rateContent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='titlelist',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='titlelist',
            name='total_rating',
            field=models.IntegerField(default=0),
        ),
    ]
