from django.db import models
from django.contrib.auth.models import User
import json
import pickle
# Create your models here.

class Userinfo(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)
    prefer = models.BinaryField(null=True)
    diet = models.BooleanField(default=False)
    hate = models.CharField(max_length=300, null=True)

    def setPrefer(self, x):
        self.prefer = pickle.dumps(x,0)

    def getPrefer(self):
        return pickle.loads(self.prefer)
    
    def __str__(self):
        return self.name
    
    
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    nation = models.CharField(max_length=100)
    primary = models.CharField(max_length=300)
    sub = models.CharField(max_length=300, null=True)
    quantity = models.CharField(max_length=100)
    tag = models.CharField(max_length=300)
    difficulty = models.CharField(max_length=100)
    ingcate = models.CharField(max_length=100)
    text = models.TextField(null=False)
    kcal = models.IntegerField()
    vector = models.BinaryField(null=True)
    imagepath = models.CharField(max_length=300, null=True)
    similars = models.BinaryField(null=True)
    
    def __str__(self):
        return self.name
    
    def setVector(self,x):
        self.vector = pickle.dumps(x,0)
        
    def getVector(self):
        x = pickle.loads(self.vector)
        return x
    
    def setSimilar(self,x):
        self.similars = pickle.dumps(x,0)
    
    def getSimilar(self):
        x = pickle.loads(self.similars)
        return x
    
    @models.permalink
    def get_absolute_url(self):
        return ('recipe_detail', [self.id])

class RecomLog(models.Model):
    user = models.ForeignKey('auth.User')
    hidden = models.BinaryField(null=True)
    recipe = models.ForeignKey(Recipe)
    aprob = models.FloatField(default=0.0)
    actual = models.IntegerField(null=True)
    
    def setHidden(self,x):
        self.hidden = pickle.dumps(x,0)
        
    def getHidden(self):
        x = pickle.loads(self.hidden)
        return x
        
    def __str__(self):
        return self.recipe