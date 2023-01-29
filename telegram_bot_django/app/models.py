from django.db import models


class UserData(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    stupid_btn = models.IntegerField(default=0)    
    fat_btn = models.IntegerField(default=0)    
    dumb_btn = models.IntegerField(default=0)    

