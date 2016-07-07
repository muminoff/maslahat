# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings
from hashids import Hashids

register = template.Library()


@register.filter
@stringfilter
def make_maslahat_id(value):
    hashids = Hashids(salt=settings.SECRET_KEY)
    return hashids.encode(int(value))
