# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.core.mail import send_mail
from django.db import models


# Create your models here.

class ProfileImg(models.Model):
    username = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_img')
