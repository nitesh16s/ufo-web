# Generated by Django 3.1.7 on 2021-05-03 07:27

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weekend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weekendadventure',
            name='details',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='details'),
        ),
    ]
