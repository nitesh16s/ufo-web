# Generated by Django 3.1.7 on 2021-04-29 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='booking_available',
        ),
    ]