# Generated by Django 3.1.7 on 2021-04-23 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import localflavor.in_.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(help_text='Profession', max_length=255)),
                ('image', models.ImageField(upload_to='team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(default='avatar.png', help_text='Profile Picture', upload_to='profile_pics')),
                ('cover_photo', models.ImageField(default='default.jpg', help_text='Cover Photo', upload_to='cover_photo')),
                ('gender', models.CharField(blank=True, choices=[('m', 'male'), ('f', 'female'), ('o', 'other')], help_text='Select your gender', max_length=1)),
                ('dob', models.DateField(default='1990-10-10', help_text='Your DOB (YYYY-MM-DD)')),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Your mobile number (e.g. +12125552368)', max_length=128, region=None)),
                ('about', models.TextField(blank=True, help_text='Tell us more about yourself...')),
                ('street', models.CharField(blank=True, help_text='Street Address', max_length=255)),
                ('house', models.CharField(blank=True, help_text='House No.', max_length=255)),
                ('city', models.CharField(blank=True, help_text='City', max_length=255)),
                ('state', localflavor.in_.models.INStateField(blank=True, max_length=2)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('slug', models.SlugField(unique=True)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_follow', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
