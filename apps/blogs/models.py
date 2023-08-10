from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from ..packages.models import Continent, Country, Activity, Package, Region
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField


class Blog(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    package = models.ForeignKey(
        Package,
        help_text='Select related package',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    continent = models.ForeignKey(
        Continent,
        help_text='Select related continent',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    country = models.ForeignKey(
        Country,
        help_text='Select related country',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    region = models.ForeignKey(
        Region,
        help_text='Select related region',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    activity = models.ManyToManyField(
        Activity,
        help_text='Select related activities',
        blank=True
    )
    title = models.CharField(
        help_text='Keep your title short upto 255',
        max_length=255,
        blank=False
    )
    content = RichTextUploadingField()
    blog_image = models.ImageField(
        help_text='Select background image (Size 450*938)',
        default='default.jpg',
        upload_to='blog_images/'
    )
    title_tag = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='add title tag here...'
    )
    seo = models.TextField(
        help_text='SEO',
        blank=True
    )
    description = models.TextField(
        help_text='add description here...',
        blank=True
    )
    keywords = models.TextField(
        help_text='add keywords here...',
        blank=True
    )
    slug = models.SlugField(unique=True, max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(
            str(self.title) + '-by-' +
            str(self.author),
            allow_unicode=True
        )
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.PROTECT,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    content = RichTextUploadingField(())
    createdAt = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.blog.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.content)[:50] + '-by-' + str(self.author)
        super(Comment, self).save(*args, **kwargs)


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.PROTECT,
        related_name='replies'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author'
    )
    content = models.TextField(('Reply...'))
    createdAt = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255)


class SaveBlog(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.PROTECT,
        related_name='savedblogs'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    is_saved = models.BooleanField(('Save this blog'), default=False)


class LikeBlog(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.PROTECT,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    is_liked = models.BooleanField(default=False)
