from django.apps import AppConfig
from django.contrib import algoliasearch
from .models import Post
from .index import PostIndex


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        Post = self.get('Post')
        algoliasearch.register(Post, PostIndex)
