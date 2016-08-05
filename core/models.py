from django.db import models


class Post(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    text = models.TextField()
    author = models.TextField()
    author_id = models.TextField(db_index=True)
    link = models.TextField()
    type = models.TextField()
    published = models.DateTimeField(db_index=True)
    reactions = models.IntegerField(db_index=True)
    comments = models.IntegerField(db_index=True)
    shares = models.IntegerField(db_index=True)
    likes = models.IntegerField(db_index=True)
    loves = models.IntegerField(db_index=True)
    wows = models.IntegerField(db_index=True)
    hahas = models.IntegerField(db_index=True)
    sads = models.IntegerField(db_index=True)
    angrys = models.IntegerField(db_index=True)
