from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from phonenumber_field.modelfields import PhoneNumberField


DIFFICULTY_LEVEL = (
    ('E', 'Easy'),
    ('M', 'Moderate'),
    ('C', 'Challenging')
)

CUURENCY_CHOICES = (
    ('₹', 'INR'),
    ('$', 'USD'),
    ('€', 'EURO')
)

GST_CHOICE = (
    ('None', 'GST data not available'),
    ('Extra', 'GST extra as applicable'),
    ('Included', 'GST included')
)

MONTHS_CHOICES = (
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December')
)


class Continent(models.Model):
    continent = models.CharField(
        help_text='Continent Name',
        max_length=255
    )
    about = RichTextUploadingField(
        help_text='Continent Short Info'
    )
    image = models.ImageField(
        help_text='Continent Image 270*240',
        default='default.jpg',
        upload_to='continent_photo'
    )
    cover = models.ImageField(
        help_text='Continent Cover 1600*597',
        default='default.jpg',
        upload_to='continent_cover'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.continent)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.continent))
        super(Continent, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('continent', args=[self.slug])


class Country(models.Model):
    continent = models.ForeignKey(
        Continent,
        on_delete=models.PROTECT
    )
    country = models.CharField(
        help_text='Country Name',
        max_length=255
    )
    about = RichTextUploadingField(
        help_text='Short info about country'
    )
    image = models.ImageField(
        help_text='Country Image 364*294',
        default='blog.jpg',
        upload_to='country_image'
    )
    cover = models.ImageField(
        help_text='Country Cover 1600*596',
        default='default.jpg',
        upload_to='country_cover'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.country)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.country))
        super(Country, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('country_packages', args=[self.slug])


class CountryHead(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text='add title here...')
    description = models.TextField(help_text='add description here...')
    keyword = models.TextField(help_text='add keyword here...')

    def __str__(self) -> str:
        return str(self.country) + ' head'


class Region(models.Model):
    region = models.CharField(
        help_text='Region Name',
        max_length=255
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.region)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.region))
        super(Region, self).save(*args, **kwargs)


class Activity(models.Model):
    activity = models.CharField(
        help_text='Activity',
        max_length=255
    )
    image = models.ImageField(
        help_text='Image related to category 1600*597',
        upload_to='activity',
        default='default.jpg'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.activity)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.activity))
        super(Activity, self).save(*args, **kwargs)

    def get_absolute_url_packages(self):
        return reverse('activity_packages', args=[self.slug])

    def get_absolute_url_blogs(self):
        return reverse('blog_category', args=[self.slug])


class ActivityHead(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text='add title here...')
    description = models.TextField(help_text='add description here...')
    keyword = models.TextField(help_text='add keyword here...')

    def __str__(self) -> str:
        return str(self.activity) + ' head'


class Category(models.Model):
    category = models.CharField(
        help_text='Category',
        max_length=255
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.category)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.category))
        super(Category, self).save(*args, **kwargs)


class Package(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT
    )
    activity = models.ManyToManyField(
        Activity,
        help_text='Select related activities.'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT
    )
    package_image = models.ImageField(
        help_text='Image 570*360',
        default='default.jpg',
        upload_to='package_img'
    )
    package_cover = models.ImageField(
        help_text='Cover 1600*596',
        upload_to='package_cover',
        default='default.jpg'
    )
    name = models.CharField(
        help_text='Package Name',
        max_length=255,
        blank=False
    )
    about = models.TextField(
        help_text='Trip Overview',
        blank=True
    )
    currency = models.CharField(
        help_text='Currency type',
        choices=CUURENCY_CHOICES,
        max_length=4,
    )
    original_cost = models.PositiveIntegerField(
        help_text='Package Original Cost',
        blank=False
    )
    group_cost = models.PositiveIntegerField(
        help_text='Package Group Cost',
        blank=False
    )
    gst_option = models.CharField(
        choices=GST_CHOICE,
        help_text='Select GST choice',
        max_length=8
    )
    difficulty = models.CharField(
        help_text='Select difficulty level',
        choices=DIFFICULTY_LEVEL,
        max_length=1,
        blank=False
    )
    duration = models.PositiveIntegerField(
        help_text='Trip Duration',
        blank=False
    )
    start_point = models.CharField(
        help_text='Starting Point',
        max_length=255,
        blank=False
    )
    end_point = models.CharField(
        help_text='End Point',
        max_length=255,
        blank=False
    )
    group_size = models.PositiveIntegerField(
        help_text='Group Size',
        blank=False
    )
    min_age = models.PositiveIntegerField(
        help_text='Min age',
        blank=False
    )
    max_alt = models.CharField(
        help_text='Maximum Altitude',
        max_length=255,
        blank=False
    )
    best_season = models.CharField(
        help_text='Best Season',
        max_length=255,
        blank=False
    )
    walking = models.CharField(
        help_text='Walking Per Day',
        blank=False,
        max_length=255
    )
    booking_option = models.BooleanField(
        help_text='Bookings only with onrequest option.',
        default=False
    )
    is_less_explored_region = models.BooleanField(
        help_text='Is it Less Explored Region Package?',
        default=False
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('package_detail', args=[self.country.slug, self.region.slug, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(
            str(self.name) + ' - ' +
            str(self.duration) + '-days')
        super(Package, self).save(*args, **kwargs)


class PackageHead(models.Model):
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text='add title here...')
    description = models.TextField(help_text='add description here...')
    keyword = models.TextField(help_text='add keyword here...')

    def __str__(self) -> str:
        return str(self.package) + ' head'


class DailyUseItem(models.Model):
    package = models.OneToOneField(Package, on_delete=models.PROTECT)
    items = RichTextUploadingField()

    def __str__(self):
        return str(self.package) + ' Daily Use Items.'


class FitnessGuide(models.Model):
    package = models.OneToOneField(Package, on_delete=models.PROTECT)
    manual = RichTextUploadingField()

    def __str__(self):
        return str(self.package) + ' Fitness Guide.'


class Itinerary(models.Model):
    package = models.OneToOneField(Package, on_delete=models.PROTECT)
    itinerary = RichTextUploadingField()

    def __str__(self):
        return str(self.package) + ' Itinerary.'


class DetailedItinerary(models.Model):
    package = models.OneToOneField(
        Package,
        on_delete=models.PROTECT
    )
    detailed_itinerary = RichTextUploadingField()

    def __str__(self):
        return str(self.package) + ' Detailed Itinerary.'


class PackageInclution(models.Model):
    package = models.OneToOneField(Package, on_delete=models.PROTECT)
    breakfast = models.PositiveIntegerField(help_text='Number of breakfasts')
    lunch = models.PositiveIntegerField(help_text='Number of lunches')
    dinner = models.PositiveIntegerField(help_text='Number of dinners')
    vehicles = models.TextField(help_text='Types of transport')
    accommodation = models.TextField(help_text='Accommodation Info')
    inclution = RichTextUploadingField(
        help_text='Complete package inclution details'
    )

    def __str__(self):
        return str(self.package) + ' Inclution.'


class PackageExclution(models.Model):
    package = models.OneToOneField(Package, on_delete=models.PROTECT)
    exclution = RichTextUploadingField(help_text='Package Exclutions')

    def __str__(self):
        return str(self.package) + ' Exclutions.'


class FAQ(models.Model):
    package = models.OneToOneField(Package, on_delete=models.PROTECT)
    faq = RichTextUploadingField()

    def __str__(self):
        return str(self.package) + ' FAQs.'


class PackageGallery(models.Model):
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='gallery/%Y/%m/%d/')

    def save(self, *args, **kwargs):
        super(PackageGallery, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.package) + ' Gallery.'


class Schedule(models.Model):
    package = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        related_name='schedules'
    )
    start_date = models.DateTimeField(help_text='Trip start date')
    end_date = models.DateTimeField(help_text='Trip end date')
    seats = models.PositiveIntegerField(help_text='Total Seats')
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return (str(self.start_date))

    def __str__(self):
        return str(self.package) + ' Schedule from ' \
            + str(self.start_date) + ' to ' + str(self.end_date)


class PackageFlexibleCost(models.Model):
    package = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        related_name='flexible_costs'
    )
    person_range = models.CharField(
        help_text='Person range',
        max_length=255
    )
    flex_cost = models.PositiveIntegerField(
        help_text='cost per person'
    )

    def __str__(self):
        return str(self.package) + ' Flexible cost for ' \
            + str(self.person_range) + ' is ' + str(self.flex_cost)


class Bookings(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.PROTECT,
        related_name='schedules'
    )
    seat_count = models.PositiveIntegerField(
        help_text='Number of seats for booking.',
        blank=False
    )
    phone_number = PhoneNumberField(
        help_text='Your mobile number (e.g. +12125552368)',
    )
    is_confirmed = models.BooleanField(
        help_text='Check this box for confirm this booking.',
        default=False
    )
    is_read = models.BooleanField(
        'I have read terms & conditions.',
        blank=False,
    )
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.package) + ' booked by ' \
            + str(self.user) + ' on ' + str(self.schedule)


class OnRequestBookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        related_name='on_request_bookings'
    )
    month = models.CharField(
        max_length=10,
        choices=MONTHS_CHOICES,
    )
    seat_count = models.PositiveIntegerField(
        help_text='Number of seats for booking.',
        blank=False
    )
    phone_number = PhoneNumberField(
        help_text='Your mobile number (e.g. +12125552368)',
    )
    short_message = models.TextField(
        help_text='Any short message or previous experiences related to mountaineering or any outdoor experiences',
        blank=True,
    )
    is_confirmed = models.BooleanField(
        help_text='Check this box for confirm this booking.',
        default=False
    )
    is_read = models.BooleanField(
        help_text='I have read terms & conditions.',
        blank=False
    )
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Package ' + str(self.package) + ' on request booking by ' + str(self.user) \
            + ' for month ' + str(self.month)


class PaymentStatus(models.Model):
    booking = models.ForeignKey(
        Bookings,
        on_delete=models.PROTECT
    )
    payment_id = models.TextField()
    order_id = models.TextField()
    signature = models.TextField()


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        help_text='Select between 1-5',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    content = RichTextUploadingField(help_text='Write your review here')
    createdAt = models.DateTimeField(auto_now_add=True)
