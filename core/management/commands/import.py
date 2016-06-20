# Django
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _l
from django.utils.dateparse import parse_datetime
from django.conf import settings

# Incogwas
from core.models import Post

# Misc
import urllib2
import json
import datetime
import csv
import time
import os
import sys


class Command(BaseCommand):
    help = "Import sample data"
    can_import_settings = True
    group_id = settings.FACEBOOK_GROUP_ID
    access_token = settings.FACEBOOK_APP_ID + "|" + settings.FACEBOOK_APP_SECRET

    def handle(self, *args, **options):
        # self.stdout.write(self.style.ERROR(_l(self.access_token)))
	self.scrapeFacebookPageFeedStatus(self.group_id, self.access_token)

    def request_until_succeed(self, url):
        req = urllib2.Request(url)
        success = False
        while success is False:
            try: 
                response = urllib2.urlopen(req)
                if response.getcode() == 200:
                    success = True
            except Exception, e:
                self.stdout.write(self.style.ERROR(e))
                time.sleep(5)
                text = "Error for URL %s: %s" % (url, datetime.datetime.now())
                self.stdout.write(self.style.ERROR(text))

        return response.read()

    # Needed to write tricky unicode correctly to csv
    def unicode_normalize(self, text):
            return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22, 0xa0:0x20 }).encode('utf-8')

    def getFacebookPageFeedData(self, group_id, access_token, num_statuses):
        
        # Construct the URL string; see http://stackoverflow.com/a/37239851 for Reactions parameters
        base = "https://graph.facebook.com/v2.6"
        node = "/%s/feed" % group_id 
        fields = "/?fields=message,link,created_time,type,name,id,comments.limit(0).summary(true),shares,reactions.limit(0).summary(true),from"
        parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
        url = base + node + fields + parameters
        
        # retrieve data
        data = json.loads(self.request_until_succeed(url))
        
        return data
        
    def getReactionsForStatus(self, status_id, access_token):

            # See http://stackoverflow.com/a/37239851 for Reactions parameters
            # Reactions are only accessable at a single-post endpoint
            
        base = "https://graph.facebook.com/v2.6"
        node = "/%s" % status_id
        reactions = "/?fields=" \
                                    "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
                                    ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
                                    ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
                                    ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
                                    ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
                                    ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
        parameters = "&access_token=%s" % access_token
        url = base + node + reactions + parameters
        
        # retrieve data
        data = json.loads(self.request_until_succeed(url))
        
        return data
        

    def processFacebookPageFeedStatus(self, status, access_token):
        
        status_id = status['id']
        status_message = '' if 'message' not in status.keys() else self.unicode_normalize(status['message'])
        link_name = '' if 'name' not in status.keys() else self.unicode_normalize(status['name'])
        status_type = status['type']
        status_link = '' if 'link' not in status.keys() else self.unicode_normalize(status['link'])
        status_author = self.unicode_normalize(status['from']['name'])
        
        status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
        status_published = status_published + datetime.timedelta(hours=-5) # EST
        status_published = status_published.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs
        
        num_reactions = 0 if 'reactions' not in status.keys() else status['reactions']['summary']['total_count']
        num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
        num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']
        
        reactions = self.getReactionsForStatus(status_id, access_token) if status_published > '2016-02-24 00:00:00' else {}
        
        num_likes = 0 if 'like' not in reactions.keys() else reactions['like']['summary']['total_count']
        num_loves = 0 if 'love' not in reactions.keys() else reactions['love']['summary']['total_count']
        num_wows = 0 if 'wow' not in reactions.keys() else reactions['wow']['summary']['total_count']
        num_hahas = 0 if 'haha' not in reactions.keys() else reactions['haha']['summary']['total_count']
        num_sads = 0 if 'sad' not in reactions.keys() else reactions['sad']['summary']['total_count']
        num_angrys = 0 if 'angry' not in reactions.keys() else reactions['angry']['summary']['total_count']
        
        # return a tuple of all processed data
        
        return (status_id, status_message, status_author, link_name, status_type, status_link,
               status_published, num_reactions, num_comments, num_shares,  num_likes,
               num_loves, num_wows, num_hahas, num_sads, num_angrys)

    def scrapeFacebookPageFeedStatus(self, group_id, access_token):
        has_next_page = True
        num_processed = 0
        scrape_starttime = datetime.datetime.now()
        
        text = "Scraping %s Facebook Group: %s\n" % (group_id, scrape_starttime)
        self.stdout.write(self.style.NOTICE(text))
        
        statuses = self.getFacebookPageFeedData(group_id, access_token, 100)
        
        while has_next_page:
            for status in statuses['data']:
                resp_data = self.processFacebookPageFeedStatus(status, access_token)
                # post_exists = Post.objects.filter(id=resp_data[0])

                post = Post()
                post.id = resp_data[0]
                post.text = resp_data[1]
                post.author = resp_data[2]
                post.type = resp_data[4]
                post.link = resp_data[5]
                post.published = parse_datetime(resp_data[6])
                post.reactions = resp_data[7]
                post.comments = resp_data[8]
                post.shares = resp_data[9]
                post.likes = resp_data[10]
                post.loves = resp_data[11]
                post.wows = resp_data[12]
                post.hahas = resp_data[13]
                post.sads = resp_data[14]
                post.angrys = resp_data[15]
                post.save()
                text = "%s post processed: %s" % (post.id, datetime.datetime.now())
                self.stdout.write(self.style.SUCCESS(text))
                
                num_processed += 1
                if num_processed % 100 == 0:
                    text = "%s posts processed: %s" % (num_processed, datetime.datetime.now())
                    self.stdout.write(self.style.SUCCESS(text))
                                        
            # if there is no next page, we're done.
            if 'paging' in statuses.keys():
                statuses = json.loads(self.request_until_succeed(statuses['paging']['next']))
            else:
                has_next_page = False
                    
            
        text = "\nDone!\n%s posts processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime)
        self.stdout.write(self.style.SUCCESS(text))
