from django.db import models


class Post(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    text = models.TextField()
    author = models.TextField()
    author_id = models.TextField()
    link = models.TextField()
    type = models.TextField()
    published = models.DateTimeField()
    reactions = models.IntegerField()
    comments = models.IntegerField()
    shares = models.IntegerField()
    likes = models.IntegerField()
    loves = models.IntegerField()
    wows = models.IntegerField()
    hahas = models.IntegerField()
    sads = models.IntegerField()
    angrys = models.IntegerField()
