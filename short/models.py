from django.db import models

class Urls (models.Model):
    original_url = models.CharField(max_length=2083,db_index=True)
    url_key = models.CharField(max_length=50,unique=True,db_index=True)
    password = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.original_url

class StatsUrl (models.Model):
    url_key = models.CharField(max_length=50,db_index=True)
    url = models.ForeignKey(Urls, on_delete=models.SET_NULL, null=True, related_name='stats')
    ip = models.CharField(max_length=30,db_index=True, null=True)
    hostname = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50, db_index=True, null=True)
    region = models.CharField(max_length=50, db_index=True, null=True)
    country = models.CharField(max_length=50, db_index=True, null=True)
    latitude = models.CharField(max_length=50,null=True)
    longitude = models.CharField(max_length=50, null=True)
    org = models.CharField(max_length=50, null=True)
    timezone = models.CharField(max_length=50, db_index=True,null=True)
    country_name = models.CharField(max_length=50, db_index=True, null=True)
    browser = models.CharField(max_length=50, db_index=True,null=True)
    os = models.CharField(max_length=50, db_index=True,null=True)
    device = models.CharField(max_length=50, db_index=True,null=True)
    is_bot = models.BooleanField(null=True)
    is_email_client = models.BooleanField(null=True)
    is_pc = models.BooleanField(null=True)
    is_tablet = models.BooleanField(null=True)
    is_mobile = models.BooleanField(null=True)
    is_touch_capable = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)