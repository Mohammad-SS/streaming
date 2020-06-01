from streaming import models
import hashlib
import time
import jdatetime as jdt
import datetime as dt
from django.db.models import Q


# This method starts signup operation
# it will check if username or phone or numberid exist in database
# password will be MD5 hexadecimal hashed .
# token is a unix time string that has been hashed with MD5 hexadecimal
# birthday will be converted to garegourian date .


def signUP(informations):
    err = doesUserExist(informations['username'],
                        informations['phone'], informations['nid'])
    if err:
        return err

    password = hashlib.md5(informations['password'].encode()).hexdigest()
    token = hashlib.md5(str(time.time()).encode()).hexdigest()
    bdate = informations['birthdate'].split("/")
    bdate = jdt.datetime(int(bdate[0]), int(bdate[1]), int(bdate[2]))
    bdate = bdate.togregorian()
    now = dt.datetime.now()
    newUser = models.User(userName=informations['username'], encryptedPassword=password, token=token,
                          fName=informations['fname'], lName=informations['lname'],
                          phone=informations['phone'], numberId=informations['nid'], birthDate=bdate,
                          educationLevel=informations['edlvl'], registerTime=now)
    newUser.save()
    return {"result": True, "code": 200, "token": newUser.token}


# this method will check if user's username , phone and number id is unique or not


def doesUserExist(username, phone, nid):
    if searchUserByUsername(username).exists():
        return {"result": False, "code": 430, "eror": "Username Exists"}
    if searchUserByPhone(phone).exists():
        return {"result": False, "code": 431, "eror": "Phone Number Exists"}
    if searchUserByNumberid(nid).exists():
        return {"result": False, "code": 430, "eror": "Number Id exists"}


# this method will search database by user's username .


def searchUserByUsername(username):
    user = models.User.objects.filter(userName=username)
    return user


# this method will search database by user's phone .


def searchUserByPhone(phone):
    user = models.User.objects.filter(phone=phone)
    return user


# this method will search database by user's numberid .


def searchUserByNumberid(nid):
    user = models.User.objects.filter(numberId=nid)
    return user


# this method will search database by user's token
def searchUserByToken(token):
    user = models.User.objects.get(token=token)
    return user


def checkForLogin(username, password):
    theUser = searchUserByUsername(username)
    password = hashlib.md5(password.encode()).hexdigest()
    if theUser.count() != 1:
        return {"result": False, "code": 630, "desc": "Username Doesnt Exist"}
    theUser = theUser[0]
    if theUser.encryptedPassword != password:
        return {"result": False, "code": 631, "desc": "Password Doesnt Match"}
    return {"result": True, "code": 200, "desc": "Login Was Success Fully", "token": theUser.token}


def doLogin(request):
    if {'username', 'password'}.issubset(request.POST):
        result = checkForLogin(request.POST['username'], request.POST['password'])
        if result['result']:
            request.session['loggedin'] = True
            request.session['token'] = result['token']
        return result
    else:
        result = {"result": False, "code": 400, "desc": "defective data received"}
        return result
