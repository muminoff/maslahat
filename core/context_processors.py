#! -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
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
                ('group_facts', {
                    'title': _('Гуруҳ фаолияти'),
                }),
            ]),
        }),
        ('about', {
            'title': _('Лойиҳа ҳақида'),
        }),
    ])

    for k, v in main_menu.items():
        path = '/{}/'.format(k)

        if request.path.endswith(path):
            v['active'] = True
            title = v['title']

        if 'dropdown' in v:
            for sk, sv in v['dropdown'].items():
                # subpath = '{}{}/'.format(path, sk)  # old code
                subpath = '/{}/'.format(sk)

                if request.path.endswith(subpath):
                    print(request.path, subpath)
                    sv['active'] = True
                    title = sv['title']

    return {
        'main_menu': main_menu,
        'title': title,
    }
