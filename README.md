# Maslahat.uz
Фейсбукдаги "Маслаҳат.уз" гуруҳи учун махсус лойиҳа

Онлайн демо версия: http://maslahat.xyz

## Лойиҳадан мақсад
Гуруҳ фаолиятини хронологик тарзда кўрсатиб бериш, гуруҳ иштирокчилари томонидан ёзилаётган постлар ва изоҳлар, уларга бўлаётган бошқа иштирокчиларнинг муносабатларини (лайк қўйиш, улашиш ва ҳ.к) статистикасини реал вақтда Фейсбукдаги маълумотлар асосида олиб бориш, гуруҳ фаолиятига умумий назар солиб таҳлил қилишга кўмаклашиш.

## Лойиҳани серверга ўрнатиш учун йўриқнома
### Талаблар

  1. Python дастурлаш тили 3.5 версияси
  2. Django веб фреймворки 1.10 версияси
  3. Postgresql маълумотлар базаси 9.5 версияси
  4. Redis структурали маълумотлар сервери 3.2 версияси

### Ўрнатиш тартиби

Facebook developer консолидан `FACEBOOK_APP_ID` ва `FACEBOOK_APP_SECRET` ни
билиб олинг. Гуруҳнинг Фейсбукдаги идентификатори `1601597320127277`.

Қуйидаги буйруқларни кетма-кетликда бажаринг.

```
$ git clone https://github.com/muminoff/maslahat.git
$ virtualenv env && source env/bin/activate.sh
$ pip install -r requirements.txt
$ createuser -s maslahat
$ createdb -O maslahat maslahat
$ export FACEBOOK_APP_ID='__FACEBOOKДАН_ОЛИНГАН__'
$ export FACEBOOK_APP_SECRET='__FACEBOOKДАН_ОЛИНГАН__'
$ export FACEBOOK_GROUP_ID=1601597320127277
$ vim maslahat/settings.py # Керакли созламаларни киритинг
$ python manage.py migrate
$ python manage.py collectstatic --noinput
$ python manage.py import
$ python manage.py runserver
```


### Disclaimer
Лойиҳа серверга ўрнатилганидан сўнг, сайтдаги ҳар қандай мазмунга эга
бўлган контент учун фақат гуруҳ админлари ва пост муаллифлари жавобгардир.

### Лицензия (License)
Лойиҳанинг код қисми GPL лицензияга эга.
