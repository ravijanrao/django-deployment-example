from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):

# Create your models here.

    user = models.OneToOneField(User) #gives the default fields

    #additional classes
    portfolio_site = models.URLField(blank=True) #user doesn't have to fill it out

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
        #need to create subdirectory called profile pics in media folder

    def __str__(self):
        return self.user.username
