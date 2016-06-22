#! -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict


def menu(request):
    title = None

    main_menu = OrderedDict([
        ('index', {
            'title': _('Сўнгги янгиликлар'),
        }),
        ('stat', {
            'title': _('Статистика'),
            'dropdown': OrderedDict([
                ('stat_yearly', {
                    'title': _('Йиллик'),
                }),
                ('stat_monthly', {
                    'title': _('Ойлик'),
                }),
                ('stat_weekdays', {
                    'title': _('Ҳафталик'),
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
