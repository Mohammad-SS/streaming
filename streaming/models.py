from django.db import models


class User(models.Model):
    userName = models.CharField(max_length=12, verbose_name="User Name")
    encryptedPassword = models.CharField(
        max_length=32, verbose_name="MD5 Hashed Password")
    token = models.CharField(max_length=32)
    lastDevice = models.CharField(
        max_length=32, verbose_name="Last Device Name")
    lastIP = models.CharField(max_length=15, verbose_name="Last Used IP")
    fName = models.CharField(max_length=15, verbose_name="First Name")
    lName = models.CharField(max_length=15, verbose_name="Last Name")
    phone = models.CharField(max_length=11, verbose_name="Phone Number")
    numberId = models.CharField(max_length=10, verbose_name="Number ID")
    birthDate = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name="Birth Date", default=None)
    educationLevel = models.CharField(
        max_length=15, verbose_name="Education Level", default=None)
    isAdmin = models.BooleanField(
        default=False, verbose_name="Is This User Admin ?")

    def __unicode__(self):
        return (self.fName + " " + self.lName)


class Conductor(models.Model):
    ITEM_TYPE = (('Sound', 'S'), ('Video', 'V'))
    name = models.CharField(max_length=30, verbose_name="Item Name")
    desc = models.TextField(verbose_name="Description")
    time = models.DateTimeField(
        auto_now=False, auto_now_add=False, verbose_name="On Air Time")
    url = models.URLField(max_length=200, verbose_name="URL")
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
    url = models.URLField(max_length=200, verbose_name="URL", default=None)
    itemType = models.CharField(
        max_length=1, choices=ITEM_TYPE, verbose_name="Type of This Item")
    category = models.CharField(max_length=35)
