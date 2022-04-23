from django.db import models
import uuid

# Create your models here.

class Handle(models.Model):
    handle = models.CharField(max_length=250)
    firstName = models.CharField(max_length=250)
    lastName = models.CharField(max_length=250)
    email = models.EmailField(primary_key=True)
    isVerified = models.BooleanField(default=False)
    uid = models.CharField(max_length=250,null=True,blank=True)
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid4())[:249]
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email

class Contest(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    date = models.DateTimeField()
    isSend = models.BooleanField(default=False)
    isParsed = models.BooleanField(default=False)
    tryCount = models.IntegerField(default=0)
    # number of Try, isSaved,


    class Meta:
        ordering = ['-date',]


class Rank(models.Model):
    handle = models.CharField(max_length=250)
    contest = models.ForeignKey(Contest, on_delete= models.CASCADE)
    globalRank = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    countryRank= models.IntegerField(null=True , blank=True)
    organization = models.CharField(max_length=250, null=True, blank=True)
    organizationRank= models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['-contest', 'globalRank']