from django.contrib.algoliasearch import AlgoliaIndex


class PostIndex(AlgoliaIndex):
    fields = ('text', 'author')
    settings = {'attributesToIndex': ['text', 'author']}
    index_name = 'maslahat'
