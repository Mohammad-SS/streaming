from django.db import models
from django_jalali.db import models as jmodel

import jdatetime


class User(models.Model):
    userName = models.CharField(max_length=18, verbose_name="User Name")
    encryptedPassword = models.CharField(
        max_length=32, verbose_name="MD5 Hashed Password")
    fName = models.CharField(max_length=15, verbose_name="First Name")
    lName = models.CharField(max_length=15, verbose_name="Last Name")
    phone = models.CharField(max_length=11, verbose_name="Phone Number")
    numberId = models.CharField(max_length=10, verbose_name="Number ID")
    birthDate = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name="Birth Date", default=None)
    educationLevel = models.CharField(
        max_length=15, verbose_name="Education Level", default=None)
    registerTime = models.DateTimeField(
        verbose_name="Register Date and Time", auto_now=False, auto_now_add=False)
    isAdmin = models.BooleanField(
        default=False, verbose_name="Is This User Admin ?")
    banned = models.BooleanField(
        default=False, verbose_name="Is This User Banned ?")
    token = models.CharField(max_length=32)

    def __str__(self):
        return (self.userName)


class ConductorItem(models.Model):
    ITEM_TYPE = (('S', 'Sound'), ('V', 'Video'))
    name = models.CharField(max_length=30, verbose_name="Item Name")
    desc = models.TextField(verbose_name="Description")
    startTime = models.DateTimeField(
        auto_now=False, auto_now_add=False, verbose_name="Start Air Time")
    duration = models.FloatField(verbose_name="Program Duration")
    itemType = models.CharField(
        max_length=1, choices=ITEM_TYPE, verbose_name="Type of This Item")

    def __str__(self):
        return self.name


class Archive(models.Model):
    ITEM_TYPE = (('S', 'Sound'), ('V', 'Video'))
    name = models.CharField(max_length=50, verbose_name="Item Name")
    desc = models.TextField(verbose_name="Description")
    time = models.TimeField(
        auto_now=False, auto_now_add=False, verbose_name="On Air Time")
    duration = models.FloatField(verbose_name="Duration of this item", default="2")
    url = models.URLField(max_length=200, verbose_name="URL", default=None)
    itemType = models.CharField(
        max_length=1, choices=ITEM_TYPE, verbose_name="Type of This Item")
    category = models.CharField(max_length=35)

    def __str__(self):
        return self.name


class Temp(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    time = models.DateTimeField()
    key = models.CharField(max_length=20)
    done = models.BooleanField(default=False)


class Log(models.Model):
    time = models.TimeField(auto_now=True)
    desc = models.TextField()
    info = models.TextField()


class Attachment(models.Model):
    type = models.CharField(max_length=5)
    uri = models.URLField()
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="avatar")
