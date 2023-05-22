from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    asset_name = models.CharField(max_length=50, verbose_name='Название актива')
    asset_serial_number = models.CharField(max_length=50, verbose_name='Серийный номер')
    asset_description = models.TextField(verbose_name='Описание')
    location = models.CharField(max_length=50, verbose_name='Место расположения')
    date_purchased = models.DateField(verbose_name='Дата приобретения')
    cost = models.CharField(max_length=50, verbose_name='Стоимость актива', default='0 руб.')

class Maintenance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата технического обслуживания')
    description = models.TextField(verbose_name='Описание')

class Repair(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата ремонта')
    description = models.TextField(verbose_name='Описание')

