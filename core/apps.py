from django.apps import AppConfig
from django.contrib import algoliasearch
from .index import PostIndex


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        Post = self.get_model('Post')
        algoliasearch.register(Post, PostIndex)
