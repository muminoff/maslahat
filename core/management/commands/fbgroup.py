# Django
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.utils import timezone

# Core
from core.models import Post

# Misc
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json
import datetime
import time
import sys
import requests


class Command(BaseCommand):
    help = "Import sample data"
    can_import_settings = True
    group_id = settings.FACEBOOK_GROUP_ID
    access_token = settings.FACEBOOK_APP_ID + \
        "|" + settings.FACEBOOK_APP_SECRET

    def handle(self, *args, **options):
        print(self.group_id, self.access_token)
        base = "https://graph.facebook.com/v2.6"
        node = "/%s/members" % self.group_id
        # fields = ""
        fields = "/?fields=id,name,updated_time"
        parameters = "&access_token=%s" % (self.access_token)
        url = base + node + fields + parameters
        resp = requests.get(url).json()
        print(resp)
        sys.exit(0)
