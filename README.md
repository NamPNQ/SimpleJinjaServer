SimpleJinjaServer
=================

Simple Jinja2 Server - The tool help frontend developer for use jinja2 template

Jinja is powerful template engine in python. If you don't know jinja, you can learn more in http://jinja.pocoo.org/. 


How to use
==========

1. First you need install python, pip
1. Install me via git with pip: `pip install git+git://github.com/NamPNQ/SimpleJinjaServer`
1. Open terminal, cd to you working directory and run comand: `python -m SimpleJinjaServer`

How to add custom filter, etc..
===============================

Make a python in your working directory, in example i make file helper.py with content

```python
__author__ = 'nampnq'

import hashlib


def add_helpers(app):

    def gravatar_filter(email, size=100, rating='g', default='retro', force_default=False,
                        force_lower=False, use_ssl=False):
        if use_ssl:
            url = "https://secure.gravatar.com/avatar/"
        else:
            url = "http://www.gravatar.com/avatar/"
        if force_lower:
            email = email.lower()
        hashemail = hashlib.md5(email).hexdigest()
        link = "{url}{hashemail}?s={size}&d={default}&r={rating}".format(
            url=url, hashemail=hashemail, size=size,
            default=default, rating=rating)
        if force_default:
            link += "&f=y"
        return link

    app.jinja_env.filters['gravatar'] = gravatar_filter

```

Make sure your defined function name add_helpers

Run command `python -m SimpleJinjaServer 5000 False helper`

Agruments
=========

First arguments is port

Second arguments is enable debug

Third agruments is filename helper


Anything else
=============

Please make issuse


Note
====

It only render file with extension html

Donate
======

If project help you, please donate me via bitcoin: 1LKyH1jTP8Agd8FakpvydCP87HQzL85cFx

I very happy, whether you donate 1 cent!

