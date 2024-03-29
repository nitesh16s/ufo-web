# Generated by Django 3.1.7 on 2021-05-03 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_remove_schedule_booking_available'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['start_date']},
        ),
        migrations.CreateModel(
            name='PackageHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='add title here...', max_length=255)),
                ('description', models.TextField(help_text='add description here...')),
                ('keyword', models.TextField(help_text='add keyword here...')),
                ('package', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='packages.package')),
            ],
        ),
        migrations.CreateModel(
            name='CountryHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='add title here...', max_length=255)),
                ('description', models.TextField(help_text='add description here...')),
                ('keyword', models.TextField(help_text='add keyword here...')),
                ('country', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='packages.country')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='add title here...', max_length=255)),
                ('description', models.TextField(help_text='add description here...')),
                ('keyword', models.TextField(help_text='add keyword here...')),
                ('activity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='packages.activity')),
            ],
        ),
    ]
