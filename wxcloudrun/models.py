from datetime import datetime

from django.db import models


# Create your models here.
class Counters(models.Model):
    id = models.AutoField
    count = models.IntegerField(max_length=11, default=0)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Counters'  # 数据库表名


# Create your models here.
class Markers(models.Model):
    id = models.AutoField
    userid = models.CharField(max_length=255, default='')
    longtitude = models.FloatField(default=0)
    latitude = models.FloatField( default=0)
    memo = models.TextField(max_length=255, default='')
    updatedAt = models.DateTimeField(default=datetime.now(),)
    #updatedAt = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Markers'  # 数据库表名