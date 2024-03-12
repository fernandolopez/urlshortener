Install
-------

```sh
poetry install
```

Run
---

```sh
poetry run ./manage.py runserver
```

Run tests
---------

```sh
poetry run ./manage.py test
```

API use
-------

### Create short url

```sh
$ curl -X POST http://127.0.0.1:8000/url/ -H 'Content-Type: application/json' -d '{"url":"http://google.com"}'

{"id":20574,"shortened_url":"http://127.0.0.1:8000/g/hoit9","url":"http://google.com","slug":"hoit9","visit_count":0,"title":null}
```

### Access url data with a given ID

```sh
$ curl http://127.0.0.1:8000/url/20574/

{"id":20574,"shortened_url":"http://127.0.0.1:8000/g/hoit9","url":"http://google.com","slug":"hoit9","visit_count":0,"title":"http://google.com/"}
```

### Short url use

```sh
$ curl -v http://127.0.0.1:8000/g/hoit9
*   Trying 127.0.0.1:8000...
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> GET /g/hoit9 HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.88.1
> Accept: */*
> 
< HTTP/1.1 302 Found
< Date: Tue, 12 Mar 2024 15:56:14 GMT
< Server: WSGIServer/0.2 CPython/3.11.4
< Content-Type: text/html; charset=utf-8
< Location: http://google.com
< X-Frame-Options: DENY
< Content-Length: 0
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
< 
* Connection #0 to host 127.0.0.1 left intact
```

### Top 100 most accessed

```sh
$ curl http://127.0.0.1:8000/url/top100/

[{"id":10759,"shortened_url":"http://127.0.0.1:8000/g/AIBN4","url":"http://google.com","slug":"AIBN4","visit_count":4,"title":"http://google.com/"},{"id":20573,"shortened_url":"http://127.0.0.1:8000/g/v2Amj","url":"http://google.com","slug":"v2Amj","visit_count":2,"title":"http://google.com/"},{"id":20574,"shortened_url":"http://127.0.0.1:8000/g/hoit9","url":"http://google.com","slug":"hoit9","visit_count":1,"title":"http://google.com/"},{"id":1,"shortened_url":"http://127.0.0.1:8000/g/hTxwG","url":"http://google.com","slug":"hTxwG","visit_count":0,"title":"Google"},{"id":3,"shortened_url":"http://127.0.0.1:8000/g/YwM5z", [...]]
```

Limitations and improve points
------------------------------

* There is no control or monitoring of how many threads are created for
title retrieval: Using Celery or even a ThreadPool are possible improvements.
* Add logging.
* A retry limit is implemented to check if a slug is available. Use a better
method to check slug availability. A posibility is to pre-generate all slugs
for a given slug length and take from avialable slugs until depleted, then
increase the lenght of the slugs.
* No credentials are required to access data or create short urls.
* Add more tests.
* Validate URLs are valid.