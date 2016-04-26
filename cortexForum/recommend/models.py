from __future__ import unicode_literals

from django.db import models

# Create your models here.

class RecommendManager(models.Manager):
    pass

class Recommend(models.Model):
    know_way=models.IntegerField(default=1)
    pub_date=models.DateTimeField(auto_now_add=True)
    satisfy_rate=models.IntegerField()
    fresh_rate=models.IntegerField()

    def __unicode__(self):
        return unicode(self.pub_date)