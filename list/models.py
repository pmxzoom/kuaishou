from django.db import models


# Create your models here.
class Billboard(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    排名 = models.CharField(max_length=1000,null=True)
    标题 = models.CharField(max_length=1000,null=True)
    热度 = models.CharField(max_length=1000,null=True)
    种类 = models.CharField(max_length=1000,null=True)



class Movie(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    片名 = models.CharField(max_length=1000,null=True)
    演员 = models.CharField(max_length=1000,null=True)
    题材 = models.CharField(max_length=1000,null=True)
    观看人数 = models.CharField(max_length=1000,null=True)


class Tube(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    剧名 = models.CharField(max_length=1000,null=True)
    简介 = models.CharField(max_length=1000,null=True)
    最近更新 = models.CharField(max_length=1000,null=True)
    观看人数 = models.CharField(max_length=1000,null=True)
