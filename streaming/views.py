from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from streaming import models, functions
import os
import datetime
import json


# this View will be called when /register/ url comes up . Required data for register user :
# userName : @string . length <= 18
# password : @string . it will be hashed by MD5 and hexa decimal
# fName & lName : @string . length <= 15
# phone : @string . length <=11
# numberId : @string . length <=10
# birthDate : @date . it must be in jalali format . it will be converted to gregorian before save to db . xxxx/xx/xx
# educationLevel : @string .length<=15

@csrf_exempt
def registerNewUser(request):
    data_received = None
    # First Check if all arguments is passed by POST data .
    if {'username', 'password', 'fname', 'lname', 'phone', 'numberid', 'birthdate', 'educationlvl'}.issubset(
            request.POST):
        data_received = {"username": request.POST['username'], "password": request.POST['password'],
                         "fname": request.POST['fname'],
                         "lname": request.POST['lname'], "nid": request.POST['numberid'],
                         "birthdate": request.POST['birthdate'], "edlvl": request.POST['educationlvl'],
                         'phone': request.POST['phone']}
    else:
        # if its not passed , so give 404 code
        jsonResponder = {"result": False, "code": 400,
                         "desc": "defective data received"}

    if data_received is not None:
        signUpRes = functions.signUP(data_received)
        if signUpRes['result']:
            request.session['loggedin'] = True

        jsonResponder = signUpRes

    # noinspection PyUnboundLocalVariable
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def loginUsers(request):
    if 'loggedin' in request.session:
        if request.session['loggedin']:
            jsonResponder = {"result": False, "code": 405, "desc": 'Already Loggedin'}
            return JsonResponse(jsonResponder, JSONEncoder, safe=False)
        else:
            return JsonResponse(functions.doLogin(request), JSONEncoder, safe=False)
    else:
        return JsonResponse(functions.doLogin(request), JSONEncoder, safe=False)


@csrf_exempt
def logOut(request):
    try:
        request.session.flush()
        return JsonResponse({"result": True, "code": 200, "desc": "You have Logged Out Success Fully"}, JSONEncoder)
    except KeyError:
        pass


@csrf_exempt
def showConductor(request):
    if 'date' in request.GET:
        split = str(request.GET['date']).split("/")
    else:
        return JsonResponse({"result": False, "code": 620, "desc": "No date received"}, JSONEncoder)
    date = datetime.datetime(int(split[0]), int(split[1]), int(split[2]))
    timeRange = [date - datetime.timedelta(days=5), date + datetime.timedelta(days=5)]
    items = functions.getConductorItem(timeRange)
    return JsonResponse({"result": True, "code": 200, "items": items}, JSONEncoder, safe=False)


@csrf_exempt
def addNewItemToConductor(request):
    username = request.POST['username']
    password = request.POST['password']
    items = json.loads(request.POST['data'])
    jsonResponder = functions.insertToConductor(username, password, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


def insertfake(request):
    for i in range(0, 30):
        name = "آیتم شماره" + str(i)
        desc = "یک آیتم فیک الکی"
        time = datetime.datetime(2020, 6, 1 + i, 15, 0)
        stype = "V"
        item = models.Archive(name=name, desc=desc, time=time.time(), duration=2, url="www.google.com" ,itemType=stype , category="Mazhabi")
        item.save()
    return HttpResponse("DONE")


@csrf_exempt
def editThisItem(request):
    username = request.POST['username']
    password = request.POST['password']
    items = json.loads(request.POST['data'])
    jsonResponder = functions.editConductorItem(username, password, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def deleteThisItem(request):
    username = request.POST['username']
    password = request.POST['password']
    items = json.loads(request.POST['data'])
    jsonResponder = functions.deleteConductorItem(username, password, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def showLive(request):
    jsonResponder = functions.getUrlTextFile()
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def changeLiveUrl(request):
    username = request.POST['username']
    password = request.POST['password']
    url = request.POST['url']
    jsonResponder = functions.changeUrlTxtFile(username, password, url)
    return JsonResponse(jsonResponder, JSONEncoder)


@csrf_exempt
def showArchive(request):
    if 'cat' not in request.POST:
        return JsonResponse({"result": False, "code": 920, "desc": "No category received"}, JSONEncoder)
    if 'size' not in request.POST:
        return JsonResponse({"result": False, "code": 921, "desc": "No size received"}, JSONEncoder)
    if 'page' not in request.POST:
        page = 1
    else:
        page = request.POST['page']
    cat = request.POST['cat']
    size = request.POST['size']
    items = functions.getArchiveItem(cat, size, page)
    return JsonResponse({"result": True, "code": 200, "items": items}, JSONEncoder, safe=False)
