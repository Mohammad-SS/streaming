from django.db import models


class User(models.Model):
    userName = models.CharField(max_length=12)
    encryptedPassword = models.CharField(max_length=32)
    token = models.CharField(max_length=32)
    lastDevice = models.CharField(max_length=32)
    lastIP = models.CharField(max_length=15)
    fName = models.CharField(max_length=15)
    lName = models.CharField(max_length=15)
    phone = models.CharField(max_length=11)
    numberId = models.CharField(max_length=10)
    birthDay = models.DateField(auto_now=False, auto_now_add=False)
    lastLicence = models.CharField(max_length=15)

    def __unicode__(self):
        return (self.fName + " " + self.lName)


class Cond(models.Model):

    class Meta:
        verbose_name = _("Cond")
        verbose_name_plural = _("Conds")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Cond_detail", kwargs={"pk": self.pk})
