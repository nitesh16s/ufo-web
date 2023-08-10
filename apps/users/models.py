from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models.signals import post_save

# third party apps
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.in_.models import INStateField
from django_countries.fields import CountryField


GENDER_CHOICE = (
    ('m', 'male'),
    ('f', 'female'),
    ('o', 'other')
)


class Profile(models.Model):
    author = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )
    profile_picture = models.ImageField(
        help_text='Profile Picture',
        default='avatar.png',
        upload_to='profile_pics'
    )
    cover_photo = models.ImageField(
        help_text='Cover Photo',
        default='default.jpg',
        upload_to='cover_photo'
    )
    gender = models.CharField(
        help_text='Select your gender',
        choices=GENDER_CHOICE,
        max_length=1,
        blank=True
    )
    dob = models.DateField(
        help_text='Your DOB (YYYY-MM-DD)',
        default='1990-10-10',
        blank=True,
        null=True
    )
    mobile = PhoneNumberField(
        help_text='Your mobile number (e.g. +12125552368)',
        blank=True,
    )
    about = models.TextField(
        help_text='Tell us more about yourself...',
        blank=True
    )
    street = models.CharField(
        help_text='Street Address',
        max_length=255,
        blank=True
    )
    house = models.CharField(
        help_text='House No.',
        max_length=255,
        blank=True
    )
    city = models.CharField(
        help_text='City',
        max_length=255,
        blank=True
    )
    state = INStateField(blank=True)
    country = CountryField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return str(self.author) + ' Profile'

    def get_age(self):
        age = (date.today() - self.dob)//timedelta(days=365.2425)
        return age

    def get_absolute_url(self):
        return reverse('profile')

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.author))
        super(Profile, self).save(*args, **kwargs)


class Team(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT)

    profession = models.CharField(
        help_text='Profession',
        max_length=255
    )
    image = models.ImageField(upload_to='team')

    def __str__(self):
        return str(self.profession)


class Follow(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='from_user'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='to_user'
    )
    is_follow = models.BooleanField(default=False)


# create profile whenever new user create an account
def save_profile(sender, instance, **kwargs):
    profile = Profile.objects.get_or_create(author=instance)


post_save.connect(save_profile, sender=User)
