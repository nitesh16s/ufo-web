# Generated by Django 3.1.7 on 2021-05-03 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(help_text='add title here...')),
                ('description', models.TextField(help_text='add description here...')),
                ('keyword', models.TextField(help_text='add keywords here...')),
                ('program', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fitness.program')),
            ],
        ),
    ]
