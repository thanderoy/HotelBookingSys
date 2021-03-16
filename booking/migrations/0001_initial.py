# Generated by Django 3.1.7 on 2021-03-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.IntegerField()),
                ('category', models.CharField(choices=[('DEL', 'DELUXE'), ('CPL', 'COUPLE'), ('PST', 'PRESIDENTIAL SUITE'), ('SGB', 'SINGLE BED')], max_length=3)),
                ('beds', models.IntegerField()),
                ('capacity', models.IntegerField()),
            ],
        ),
    ]