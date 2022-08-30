# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import AbstractUser

managed=True
class Point(models.Model):
    alt = models.FloatField()
    log = models.FloatField()

    class Meta:
        managed = managed
        db_table = 'point'

class User(AbstractUser):
    typeCompte= models.CharField(max_length=100, blank=True, default='client')
    tlf=models.CharField(max_length=100,unique=True)
    is_connected=models.BooleanField(default=False)
    is_free=models.BooleanField(default=True)
    firebaseID=models.CharField(max_length=200,blank=True,null=True)
    point_actuelle = models.ForeignKey(Point, models.DO_NOTHING, null=True,db_column='point')
    class Meta:
        verbose_name_plural = '1. Add Users'
    def __str__(self):
        return self.username

class Client(models.Model):
    user=models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    typeclient = models.CharField(max_length=200,default='simple')  # Field name made lowercase.
    #client_tlf = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = managed
        db_table = 'client'
 

class Driver(models.Model):
    user=models.OneToOneField(User, related_name='driver',on_delete=models.CASCADE)
    #driver_tlf = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = managed
        db_table = 'driver'


class Amite(models.Model):
    id_client = models.ForeignKey('Client', models.DO_NOTHING, db_column='id_client')
    id_driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='id_driver')

    class Meta:
        managed = managed
        db_table = 'amite'
        #unique_together = (('id_client', 'id_driver'),)



class Category(models.Model):
    cat_name = models.CharField(max_length=100, blank=True, null=True)
    path_cat = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = managed
        db_table = 'category'


class Coursa(models.Model):
    date_dapart    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_arrive    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    arrive         = models.ForeignKey('Point', models.DO_NOTHING, db_column='arrive',related_name='arrive', blank=True, null=True)
    client         = models.ForeignKey(Client, models.DO_NOTHING, db_column='client', blank=True, null=True)
    depart         = models.ForeignKey('Point', models.DO_NOTHING, db_column='depart',related_name='depart', blank=True, null=True)
    voiture        = models.ForeignKey('Voiture', models.DO_NOTHING, db_column='voiture', blank=True, null=True)
    
    class Meta:
        managed = managed
        db_table = 'coursa'




class Docs(models.Model):
    path_doc = models.CharField(max_length=100, blank=True, null=True)
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client', blank=True, null=True)
    id_driver = models.ForeignKey('Driver', models.DO_NOTHING, db_column='id_driver', blank=True, null=True)
    id_voiture = models.ForeignKey('Voiture', models.DO_NOTHING, db_column='id_voiture', blank=True, null=True)

    class Meta:
        managed = managed
        db_table = 'docs'




class Marque(models.Model):
    marque_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = managed
        db_table = 'marque'


class Model(models.Model):
    model_name = models.CharField(max_length=100, blank=True, null=True)
    id_marque = models.ForeignKey(Marque, models.DO_NOTHING, db_column='id_marque', blank=True, null=True)

    class Meta:
        managed = managed
        db_table = 'model'





class Tracking(models.Model):
    coursa = models.OneToOneField(Coursa, models.DO_NOTHING, db_column='coursa', primary_key=True)
    point = models.ForeignKey(Point, models.DO_NOTHING, null=True,db_column='point')
    #bsh na3Rf wa9t li kan fiiha 
    time=models.DateTimeField( editable=False,auto_now_add=True, null=True, blank=True)
    class Meta:
        managed = managed
        db_table = 'tracking'
        unique_together = (('coursa', 'point'),)




class Voiture(models.Model):
    matrciule = models.CharField(max_length=100, blank=True, null=True,unique=True)
    id_cat = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_cat', blank=True, null=True)
    id_driver = models.ForeignKey(Driver, models.DO_NOTHING, db_column='id_driver', blank=True, null=True)
    id_model = models.ForeignKey(Model, models.DO_NOTHING, db_column='id_model', blank=True, null=True)
    occupe=models.BooleanField(default=False)
    class Meta:
        managed = managed
        db_table = 'voiture'