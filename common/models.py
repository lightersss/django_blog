from django.db import models
from django.contrib.auth.models import AbstractUser ,User
# Create your models here.


class MyUser(AbstractUser):
    mobile=models.CharField(max_length=100,db_column='mobile_number',verbose_name='电话号码',blank=True)
    class Meta:
        db_table='myuser'
