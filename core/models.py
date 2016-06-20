from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Post(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    text = models.TextField()
    author = models.TextField()
    link = models.TextField()
    type = models.TextField()
    published = models.DateTimeField()
    reactions = models.IntegerField()
    comments = models.IntegerField()
    shares = models.IntegerField()
    likes = models.IntegerField()
    loves = models.IntegerField()
    hahas = models.IntegerField()
    sads = models.IntegerField()
    angrys = models.IntegerField()
