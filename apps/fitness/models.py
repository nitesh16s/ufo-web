from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from phonenumber_field.modelfields import PhoneNumberField


CUURENCY_CHOICES = (
    ('₹', 'INR'),
    ('$', 'USD'),
    ('€', 'EURO')
)


class Program(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(help_text='Program name', max_length=255)
    currency = models.CharField(
        help_text='Currency', choices=CUURENCY_CHOICES, max_length=4)
    cost = models.PositiveIntegerField(help_text='Program cost')
    description = RichTextUploadingField(help_text='description')
    program_image = models.ImageField(
        upload_to='fitness', default='default.jpg')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Program, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('program_detail', args=[self.slug])


class ProgramHead(models.Model):
    program = models.OneToOneField(Program, on_delete=models.CASCADE)
    title = models.TextField(help_text='add title here...')
    description = models.TextField(help_text='add description here...')
    keyword = models.TextField(help_text='add keywords here...')

    def __str__(self) -> str:
        return str(self.program) + ' head'


class ProgramBooking(models.Model):
    program = models.ForeignKey(
        Program,
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
        return str(self.program) + '-booked-by-' + str(self.first_name)
