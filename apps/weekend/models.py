from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


class WeekendAdventure(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(help_text='name', max_length=255)
    details = RichTextUploadingField(help_text='details')
    image = models.ImageField(default='default.jpg', upload_to='weekend')
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(WeekendAdventure, self).save(*args, **kwargs)


class WeekendAdventureBooking(models.Model):
    weekend_program = models.ForeignKey(
        WeekendAdventure,
        on_delete=models.PROTECT
    )
    first_name = models.CharField(
        help_text='Your first name',
        max_length=255,
    )
    last_name = models.CharField(
        help_text='Your last name',
        max_length=255,
    )
    email = models.EmailField(
        help_text='Your email address',
        blank=False,
    )
    phone_number = PhoneNumberField(
        help_text='Your mobile number (e.g. +12125552368)',
        blank=False,
    )
    short_message = models.TextField(
        help_text='any short message',
        blank=True
    )

    def __str__(self):
        return str(self.weekend_program) + '-booked-by-' + str(self.first_name)
