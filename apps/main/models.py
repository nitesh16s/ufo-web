from django.db import models
from django.contrib.auth.models import User


class Query(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    query = models.TextField(help_text='What is your query?')

    def __str__(self):
        return str(self.query)


class Answer(models.Model):
    query = models.ForeignKey(Query, on_delete=models.PROTECT)
    answer = models.TextField(help_text='answer for the query')

    def __str__(self):
        return str(self.answer)


class Sponsers(models.Model):
    name = models.CharField(('Sponser name'), max_length=255)
    image = models.ImageField(upload_to='sponsers')
    url = models.URLField(help_text='link to the sponser website.', default='', blank=True)

    def __str__(self):
        return str(self.name)


class WorkWithUs(models.Model):
    email = models.EmailField(
        help_text='Your email',
        null=False, blank=False,
        unique=True)

    def __str__(self):
        return str(self.email)
