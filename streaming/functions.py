from streaming import models
import hashlib
import jdatetime as jdt
import datetime as dt
import os


# This method starts signup operation
# it will check if username or phone or numberid exist in database
# password will be MD5 hexadecimal hashed .
# birthday will be converted to gregorian date .
# returns standard json response
def signUP(informations):
    err = doesUserExist(informations['username'],
                        informations['phone'], informations['nid'])
    if err:
        return err

    password = hashlib.md5(informations['password'].encode()).hexdigest()
    bdate = informations['birthdate'].split("/")
    bdate = jdt.datetime(int(bdate[0]), int(bdate[1]), int(bdate[2]))
    bdate = bdate.togregorian()
    now = dt.datetime.now()
    newUser = models.User(userName=informations['username'], encryptedPassword=password,
                          fName=informations['fname'], lName=informations['lname'],
                          phone=informations['phone'], numberId=informations['nid'], birthDate=bdate,
                          educationLevel=informations['edlvl'], registerTime=now)
    newUser.save()
    return {"result": True, "code": 200}


# this method will check if user's username , phone and number id is unique or not
# returns json error in standard type if user exist . otherwise returns None .
def doesUserExist(username, phone, nid):
    if searchUserByUsername(username).exists():
        return {"result": False, "code": 430, "eror": "Username Exists"}
    if searchUserByPhone(phone).exists():
        return {"result": False, "code": 431, "eror": "Phone Number Exists"}
    if searchUserByNumberid(nid).exists():
        return {"result": False, "code": 430, "eror": "Number Id exists"}


# this method will search database by user's username .
# returns User
def searchUserByUsername(username):
    user = models.User.objects.filter(userName=username)
    return user


# this method will search database by user's phone .
# returns User
def searchUserByPhone(phone):
    user = models.User.objects.filter(phone=phone)
    return user


# this method will search database by user's numberid .
# returns User
def searchUserByNumberid(nid):
    user = models.User.objects.filter(numberId=nid)
    return user


# the method will check if passed data is correct or not .
# returns JSON with standard response format

def checkForLogin(username, password):
    theUser = searchUserByUsername(username)
    password = hashlib.md5(password.encode()).hexdigest()
    if theUser.count() != 1:
        return {"result": False, "code": 630, "desc": "Username Doesnt Exist"}
    theUser = theUser[0]
    if theUser.encryptedPassword != password:
        return {"result": False, "code": 631, "desc": "Password Doesnt Match"}
    return {"result": True, "code": 200, "desc": "Login Was Success Fully", "username": theUser.userName,
            "fname": theUser.fName, "lname": theUser.lName, "edlvl": theUser.educationLevel,
            "birthdate": jdt.date.fromgregorian(date=theUser.birthDate).strftime("%Y/%m/%d"),
            "registertime": jdt.date.fromgregorian(date=theUser.registerTime).strftime("%Y/%m/%d")}


# this method will be called whenever we need to login users . it just handle sessions and uses @checkForLogin method .
# returns JSON with standard response format
def doLogin(request):
    if {'username', 'password'}.issubset(request.POST):
        result = checkForLogin(request.POST['username'], request.POST['password'])
        if result['result']:
            request.session['loggedin'] = True
        return result
    else:
        result = {"result": False, "code": 400, "desc": "defective data received"}
        return result


# this method will check if this user is admin or not .
# returns True and False .
def checkForAdmin(username, password):
    if not checkForLogin(username, password)['result']:
        return False
    password = hashlib.md5(password.encode()).hexdigest()
    result = models.User.objects.get(userName=username, encryptedPassword=password)
    return result.isAdmin


# this method will returns conductor items within passed time range .
# returns ConductorItem .
def getConductorItem(timeRange):
    items = models.ConductorItem.objects.all().filter(startTime__range=timeRange).order_by("startTime")
    itemsList = items.values()
    for item in itemsList:
        item['startTime'] = jdt.datetime.fromgregorian(date=item['startTime']).strftime("%Y/%m/%d - %H:%M ")
    itemsList = list(itemsList)
    return itemsList


# this method will check if passed username and password is belong to an admin or not .
# if belongs , it will insert passed json items .
# returns standard json respond
def insertToConductor(username, password, items):
    if checkForAdmin(username, password):
        for i in items:
            item = items[i]
            splitedTime = item.get("time").split(":")
            splitedDate = item.get("date").split("/")
            print(splitedDate)
            print(splitedTime)
            date = jdt.datetime(int(splitedDate[0]), int(splitedDate[1]), int(splitedDate[2]), int(splitedTime[0]),
                                int(splitedTime[1]))
            date = date.togregorian()
            newItem = models.ConductorItem(name=item.get("name"), desc=item.get("desc"), startTime=date,
                                           duration=int(item.get("duration")), itemType=item.get("type"))
            newItem.save()
            if not newItem.id:
                return {"result": False, "code": 607, "desc": "item " + i + " is corrupted"}
        return {"result": True, "code": 608, "desc": "items inserted successfully"}
    else:
        return {"result": False, "code": 666, "desc": "User is not admin"}


# this mehod will find conductor item by id .
# it returns ConductorItem
def getConductorItemById(itemid):
    item = models.ConductorItem.objects.filter(id=itemid)
    return item


# this method will edit conductor if passed username and password belongs to an admin .
# it will update database with passed items .
# it returns standard json response
def editConductorItem(username, password, items):
    if checkForAdmin(username, password):
        number = 0
        for i in items:
            item = items[i]
            # print(items[i]['id'])
            db_item = getConductorItemById(item.get("id"))
            splitedTime = item.get("time").split(":")
            splitedDate = item.get("date").split("/")
            date = jdt.datetime(int(splitedDate[0]), int(splitedDate[1]), int(splitedDate[2]), int(splitedTime[0]),
                                int(splitedTime[1]))
            date = date.togregorian()
            updatedRows = db_item.update(startTime=date, name=item.get('name'), desc=item.get('desc'),
                                         duration=item.get('duration'), itemType=item.get('type'))
            number = number + updatedRows
        if number == len(items):
            return {"result": True, "code": 609, "desc": str(int(number)) + "items edited successfully"}
        else:
            return {"result": True, "code": 610,
                    "desc": "failed to update " + str(len(items) - int(number)) + " records"}
    else:
        return {"result": False, "code": 666, "desc": "User is not admin"}


# this method will delete an item from conductor if passed username and password belong to an admin .
# it returns standard json response
def deleteConductorItem(username, password, items):
    if checkForAdmin(username, password):
        number = 0
        for i in items:
            item = items[i]
            db_item = getConductorItemById(item.get("id"))
            db_item.delete()
            number = number + db_item.count()
        if len(items) == number and not number == 0:
            return {"result": True, "code": 611, "desc": str(int(number)) + " items deleted successfully"}
        else:
            if number == 0:
                return {"result": False, "code": 613,
                        "desc": "no data passed"}
            return {"result": True, "code": 612,
                    "desc": "failed to delete " + str(len(items) - int(number)) + " records"}
    else:
        return {"result": False, "code": 666, "desc": "User is not admin"}


# this method will read the text file in streaming directory
# returns standard json response
def getUrlTextFile():
    module_dir = os.path.dirname(__file__)
    file_dir = os.path.join(module_dir, "live_url.txt")
    try:
        date_file = open(file_dir, 'r')
        data = date_file.read()
        return {"result": True, "code": 200, "url": data}
    except IOError:
        return {"result": False, "code": 701, "desc": "File Not Found"}


# this method will write passed url in streaming text file if username and password belong to an admin
# it wil return standard json response
def changeUrlTxtFile(username, password, url):
    if not checkForAdmin(username, password):
        print(checkForAdmin(username, password))
        return {"result": False, "code": 666, "desc": "User is not admin"}

    module_dir = os.path.dirname(__file__)
    file_dir = os.path.join(module_dir, "live_url.txt")
    try:
        data_file = open(file_dir, 'w+')
        data_file.write(url)
        data_file.close()
        return {"result": True, "code": 200, "desc": "url has been updated"}
    except IOError:
        return {"result": False, "code": 701, "desc": "File Not Found"}


def getArchiveItem(cat, size, page):
    startPoint = (int(page) - 1) * int(size)
    endPoint = startPoint + int(size)
    items = models.Archive.objects.filter(category=cat).order_by('id')[startPoint:endPoint]
    itemsList = items.values()
    for item in itemsList:
        item['time'] = item['time'].strftime("%H:%M")
    itemsList = list(itemsList)
    return itemsList
