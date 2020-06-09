from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from streaming import models, functions, enums
import datetime
import json
import jdatetime as jdt
import datetime as dt


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
    if "loggedin" and "token" in request.session:
        user = functions.searchUserByToken(request.session['token'])
        functions.createLog("loggedin user tried to signup again", {"user": user, "data": request.POST})
        jsonResponder = {"result": False, "code": 400,
                         "desc": "you are signedin . please logout first"}
        return JsonResponse(jsonResponder, JSONEncoder)

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
        functions.createLog("one user trying to signup , but defective defective", {"data": request.POST})
        jsonResponder = {"result": False, "code": 400,
                         "desc": "defective data received"}

    if data_received is not None:
        signUpRes = functions.signUP(data_received)
        if signUpRes['result']:
            request.session['loggedin'] = True
            request.session['token'] = signUpRes['token']
        jsonResponder = signUpRes

    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def loginUsers(request):
    if 'loggedin' in request.session:
        functions.createLog(enums.getDescription(405), request.POST)
        jsonResponder = {"result": False, "code": 405, "desc": enums.getErrors(405)}
        return JsonResponse(jsonResponder, JSONEncoder, safe=False)
    else:
        return JsonResponse(functions.doLogin(request), JSONEncoder, safe=False)


@csrf_exempt
def logOut(request):
    if 'loggedin' not in request.session:
        functions.createLog("user tried to logout , but not logged in before", {"data": request.POST})
        return JsonResponse({"result": False, "code": 404, "desc": "You are not loggedin"}, JSONEncoder)
    try:
        user = functions.searchUserByToken(request.session['token'])
        request.session.flush()
        functions.createLog("user signed out", {"user": user})
        return JsonResponse({"result": True, "code": 200, "desc": "You have Logged Out Success Fully"}, JSONEncoder)
    except KeyError:
        pass


@csrf_exempt
def showConductor(request):
    if 'date' in request.GET:
        split = str(request.GET['date']).split("/")
    else:
        return JsonResponse({"result": False, "code": 620, "desc": "No date received"}, JSONEncoder)
    if 'startnumber' and 'endnumber' in request.GET:
        startn = int(request.GET['startnumber'])
        endn = int(request.GET['endnumber'])
    else:
        startn = 0
        endn = 7
    date = datetime.datetime(int(split[0]), int(split[1]), int(split[2]))
    timeRange = [date - datetime.timedelta(days=startn), date + datetime.timedelta(days=endn)]
    items = functions.getConductorItem(timeRange)
    return JsonResponse({"result": True, "code": 200, "items": items}, JSONEncoder, safe=False)


@csrf_exempt
def addNewItemToConductor(request):
    # username = request.POST['username']
    # password = request.POST['password']
    user = models.User.objects.get(token=request.session['token'])
    items = json.loads(request.POST['data'])
    jsonResponder = functions.insertToConductor(user.userName, user.encryptedPassword, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


def insertfake(request):
    for i in range(0, 30):
        name = "آیتم شماره" + str(i)
        desc = "یک آیتم فیک الکی"
        time = datetime.datetime(2020, 6, 1 + i, 15, 0)
        stype = "V"
        item = models.Archive(name=name, desc=desc, time=time.time(), duration=2, url="www.google.com", itemType=stype,
                              category="Mazhabi")
        item.save()
    return HttpResponse("DONE")


@csrf_exempt
def editThisConductorItem(request):
    # username = request.POST['username']
    # password = request.POST['password']
    user = models.User.objects.get(token=request.session['token'])
    items = json.loads(request.POST['data'])
    jsonResponder = functions.editConductorItem(user.userName, user.encryptedPassword, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def deleteThisConductorItem(request):
    # username = request.POST['username']
    # password = request.POST['password']
    user = models.User.objects.get(token=request.session['token'])
    items = json.loads(request.POST['data'])
    jsonResponder = functions.deleteConductorItem(user.userName, user.encryptedPassword, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def showLive(request):
    jsonResponder = functions.getUrlTextFile()
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def changeLiveUrl(request):
    # username = request.POST['username']
    # password = request.POST['password']
    url = request.POST['url']
    user = models.User.objects.get(token=request.session['token'])
    jsonResponder = functions.changeUrlTxtFile(user.userName, user.encryptedPassword, url)
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


@csrf_exempt
def addNewItemToArchive(request):
    # username = request.POST['username']
    # password = request.POST['password']
    items = json.loads(request.POST['data'])
    user = models.User.objects.get(token=request.session['token'])
    jsonResponder = functions.insertToArchive(user.userName, user.encryptedPassword, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def editThisArchiveItem(request):
    # username = request.POST['username']
    # password = request.POST['password']
    items = json.loads(request.POST['data'])
    user = models.User.objects.get(token=request.session['token'])
    jsonResponder = functions.editArchiveItem(user.userName, user.encryptedPassword, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def deleteThisArchiveItem(request):
    # username = request.POST['username']
    # password = request.POST['password']
    items = json.loads(request.POST['data'])
    user = models.User.objects.get(token=request.session['token'])
    jsonResponder = functions.deleteArchiveItem(user.userName, user.encryptedPassword, items)
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def forgetPassword(request):
    phone = request.POST['phone']
    result = functions.createTempKey(phone)
    if result:
        return JsonResponse({"result": True, "code": 200, "desc": "Code has been sent successfully"}, JSONEncoder,
                            safe=False)
    else:
        return JsonResponse({"result": True, "code": 909, "desc": "Could not send Code"}, JSONEncoder, safe=False)


@csrf_exempt
def changePassword(request):
    key = request.POST['key']
    newPassword = request.POST['password']
    result = functions.updatePassword(key, newPassword)
    return JsonResponse(result, JSONEncoder, safe=False)


@csrf_exempt
def changeUserDataByUser(request):
    result = functions.changeThisUserDataByUser(request)
    return JsonResponse(result, JSONEncoder, safe=False)


@csrf_exempt
def changeUserDataByAdmin(request):
    result = functions.changeThisUserDataByAdmin(request)
    return JsonResponse(result, JSONEncoder, safe=False)


@csrf_exempt
def deleteAccountByUser(request):
    # print(result)
    if "loggedin" and "token" in request.session:
        operator = models.User.objects.filter(token=request.session['token'])
        if 'userid' in request.POST:
            user = models.User.objects.filter(id=request.POST['userid'])
            if user.count() != 1:
                functions.createLog("deleting operation failed beqause user didnt found",
                                    {"userid": request.POST['userid'], "operator": operator})
                return JsonResponse({"result": False, "desc": "user didnt found", "code": 698},
                                    JSONEncoder)
        else:
            user = operator
        if operator[0] != user[0] and not operator[0].isAdmin:
            functions.createLog("not allowed operator failed to delete user", {"user": user, "operator": operator})
            return JsonResponse(
                {"result": False, "code": 667, "error": "you dont have permissions to delete this user"}, JSONEncoder)
        if operator[0].isAdmin and operator[0] == user[0]:
            functions.createLog("admin tried to delete his self . this is only possible from database",
                                {"admin": operator})
            return JsonResponse(
                {"result": False, "code": 697, "error": "you dont have permissions to delete this user"}, JSONEncoder)

        try:
            user.delete()
            functions.createLog("user has been deleted user successfully", {"user": user, "operator": operator})
            return JsonResponse({"result": True, "desc": "Account Has been deleted success fully", "code": 200},
                                JSONEncoder)
        except Exception as e:
            functions.createLog("something went wrong when operator tried to delete user",
                                {"user": user, "operator": operator, "error": e})
            return JsonResponse(
                {"result": True, "desc": "something went wrong when operator tried to delete user", "code": 200,
                 "error": e}, JSONEncoder)

    else:
        return JsonResponse({"result": False, "desc": "Could not delete account", "code": 1003}, JSONEncoder)


@csrf_exempt
def deleteAccountByAdmin(request):
    result = functions.checkForAdmin(request.POST['username'], request.POST['password'])
    # print(result)
    if result:
        user = models.User.objects.filter(id=request.POST['userId'])
        user.delete()
        return JsonResponse({"result": True, "desc": "This Account Has been deleted success fully", "code": 200},
                            JSONEncoder)
    else:
        return JsonResponse({"result": False, "desc": "Could not delete account", "code": 1003}, JSONEncoder)


@csrf_exempt
def getUserData(request):
    user = models.User.objects.get(token=request.session['token'])
    birthDate = jdt.datetime.fromgregorian(datetime=user.birthDate).strftime("%Y/%m/%d")
    registerTime = jdt.datetime.fromgregorian(datetime=user.registerTime).strftime("%Y/%m/%d")
    jsonResponder = {"code": 200, "desc": "data recived successfully",
                     "data": {"userName": user.userName, "firstName": user.fName, "lastName": user.lName,
                              "phone": user.phone, "numberId": user.numberId, "birthDate": birthDate,
                              "educationLevel": user.educationLevel, "registerTime": registerTime, }}
    return JsonResponse(jsonResponder, JSONEncoder)


@csrf_exempt
def getAllUsers(request):
    operator = models.User.objects.get(token=request.session['token'])
    if not operator.isAdmin:
        functions.createLog("not allowed operator failed to get users list", {"user": operator})
        return JsonResponse(
            {"result": False, "code": 666, "error": "you dont have permissions"}, JSONEncoder)
    else:
        users = list(models.User.objects.filter().all().values('userName', 'id', 'numberId', 'phone'))
        return JsonResponse(
            {"result": True, "code": 200, "data": users}, JSONEncoder)