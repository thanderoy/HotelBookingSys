# Generated by Django 3.1.7 on 2021-05-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
