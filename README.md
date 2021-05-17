# Django_bitly_clone

## Technical task
It is required to implement a web application - an analog of __bit.ly__ and similar systems.

The application contains one page on which:
The form in which you can enter the URL, which should be shortened
A tablet with all abbreviated URLs (with pagination) of this user

Mandatory requirements:
+ The application does NOT contain authorization
+ The application tracks users by session
+ Data is stored in MySQL
+ When entering a compressed URL, the application redirects to the corresponding URL (which was compressed)
+ The user can optionally specify it _subpart_. If such a <subpart> is already in use, you need to inform the user about it.
+ Implementation on Django
+ Caching redirects in Redis
+ Clear old rules on schedule
+ Docker-compose up to start the service and all the dependencies

## Installing

First you need run command
```
$ docker-compose up -d --build
```

Then for create tables in database

```
$ docker-compose web python /app/manage.py migrate
```
