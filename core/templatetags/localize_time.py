# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def uzbekify_daymonthyear(value):
    month_names_in_uzbek = [
            'январь', 'февраль', 'март',
            'апрель', 'май', 'июнь',
            'июль', 'август', 'сентябрь',
            'октябрь', 'ноябрь', 'декабрь'
            ]
    day, month, year = value.split('-')
    return '{day} {month}, {year} йил'.format(
            day=int(day),
            month=month_names_in_uzbek[int(month)-1],
            year=year
            )


@register.filter
@stringfilter
def uzbekify_monthyear(value):
    month_names_in_uzbek = [
            'январь', 'февраль', 'март',
            'апрель', 'май', 'июнь',
            'июль', 'август', 'сентябрь',
            'октябрь', 'ноябрь', 'декабрь'
            ]
    month, year = value.split('-')
    return '{month}, {year} йил'.format(
            month=month_names_in_uzbek[int(month)-1],
            year=year
            )


@register.filter
@stringfilter
def uzbekify_time(value):
    time_names_in_uzbek = [ 
            'Тунги соат 12', 'Тунги соат 1', 'Тунги соат 2', 'Тунги соат 3',
            'Эрталабки соат 4', 'Эрталабки соат 5', 'Эрталабки соат 6', 'Эрталабки соат 7',
            'Эрталабки соат 8', 'Эрталабки соат 9', 'Эрталабки соат 10', 'Эрталабки соат 11',
            'Туш вақти', 'Тушдан кейин соат 1', 'Тушдан кейин соат 2', 'Тушдан кейин соат 3',
            'Кечки соат 4', 'Кечки соат 5', 'Кечки соат 6', 'Кечки соат 7',
            'Кечки соат 8', 'Кечки соат 9', 'Кечки соат 10', 'Кечки соат 11',
            ]
    return time_names_in_uzbek[int(float(value))]


@register.filter
@stringfilter
def uzbekify_weekday(value):
    weekday_names_in_uzbek = [ 'якшанба', 'душанба', 'сешанба', 'чоршанба', 'пайшанба', 'жума', 'шанба' ]
    return weekday_names_in_uzbek[int(float(value))]


@register.filter
@stringfilter
def uzbekify_month(value):
    month_names_in_uzbek = [ 
            'январь', 'февраль', 'март',
            'апрель', 'май', 'июнь',
            'июль', 'август', 'сентябрь',
            'октябрь', 'ноябрь', 'декабрь' 
            ]
    return month_names_in_uzbek[int(float(value))-1]
