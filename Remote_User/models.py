from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    gender= models.CharField(max_length=30)
    address= models.CharField(max_length=30)


class wind_speed_forecasting(models.Model):

    Fid= models.CharField(max_length=3000)
    Latitude= models.CharField(max_length=3000)
    Langitude= models.CharField(max_length=3000)
    Fdate= models.CharField(max_length=3000)
    Wind_Speed= models.CharField(max_length=3000)
    First_Indicator= models.CharField(max_length=3000)
    RAIN= models.CharField(max_length=3000)
    Second_Indicator= models.CharField(max_length=3000)
    Max_Temp= models.CharField(max_length=3000)
    Third_Indicator= models.CharField(max_length=3000)
    Min_temp= models.CharField(max_length=3000)
    Min_grass_temp= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



