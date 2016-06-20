from django.contrib.algoliasearch import AlgoliaIndex


class PostIndex(AlgoliaIndex):
    fields = ('text', 'author', 'likes')
    settings = {'attributesToIndex': ['text', 'author', 'likes']}
    index_name = 'maslahat'
