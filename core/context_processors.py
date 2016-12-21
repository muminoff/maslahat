#! -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from collections import OrderedDict


def menu(request):
    title = None

    main_menu = OrderedDict([
        ('feed', {
            'title': _('Янги постлар'),
        }),
        ('stat', {
            'title': _('Статистика'),
            'dropdown': OrderedDict([
                ('stat_yearly', {
                    'title': _('Йиллар бўйича'),
                }),
                ('stat_monthly', {
                    'title': _('Ойлар бўйича'),
                }),
                ('stat_weekdays', {
                    'title': _('Ҳафта кунлари бўйича'),
                }),
            ]),
        }),
        ('top', {
            'title': _('Рейтинг'),
            'dropdown': OrderedDict([
                ('top_posters', {
                    'title': _('Энг кўп пост ёзганлар'),
                }),
                ('top_shared_posts', {
                    'title': _('Энг кўп улашилган постлар'),
                }),
                ('top_commented_posts', {
                    'title': _('Энг кўп муҳокама бўлган постлар'),
                }),
                ('top_liked_posts', {
                    'title': _('Кўпчиликка ёққан постлар'),
                }),
            ]),
        }),
        ('facts', {
            'title': _('Фактлар'),
            'dropdown': OrderedDict([
                ('group_activity', {
                    'title': _('Гуруҳ фаоллиги'),
                }),
                ('group_growth', {
                    'title': _('Гуруҳнинг ўсиши'),
                }),
            ]),
        }),
        ('about', {
            'title': _('Лойиҳа ҳақида'),
        }),
    ])

    for k, v in main_menu.items():

        if reverse(k) == request.path:
            print("================>", reverse(k))
            v['active'] = True
            title = v['title']

        if 'dropdown' in v:
            for sk, sv in v['dropdown'].items():
                print("================>", reverses(k))

                if reverse(sk) == request.path:
                    sv['active'] = True
                    title = sv['title']

    return {
        'main_menu': main_menu,
        'title': title,
    }
