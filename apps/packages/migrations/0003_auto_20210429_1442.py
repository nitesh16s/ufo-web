# Generated by Django 3.1.7 on 2021-04-29 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_remove_schedule_booking_available'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['start_date']},
        ),
    ]