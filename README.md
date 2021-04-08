# Facebook_Scrapy
## requirements
- scrapy
- requests
- bs4

## usage
- set your facebook email and password in facebook_scrapy/settings.py
```python
## facebook_scrapy/settings.py
EMAIL = 'your_email@example.com'
PASSWORD = 'your_password'
```
- set target user id in facebook_scrapy/spiders/facebook.py
```python
## facebook_scrapy/spiders/facebook.py
USER_ID = 'target user id'
```
- crawl target user id
```shell
$ scrapy crawler facebook
```