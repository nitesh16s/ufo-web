# Generated by Django 3.1.7 on 2021-04-23 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210423_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, default='1990-10-10', help_text='Your DOB (YYYY-MM-DD)', null=True),
        ),
    ]
