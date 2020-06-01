from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from streaming import models, functions


# this View will be called when /register/ url comes up . Required data for register user :
# userName : @string . lenght <= 18
# password : @string . it will be hashed by MD5 and hexa decimal
# fName & lName : @string . length <= 15
# phone : @string . length <=11
# numberId : @string . length <=10
# birthDate : @date . it must be in jalali format . it will be converted to garegourian before save to db . xxxx/xx/xx
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
            request.session['token'] = signUpRes['token']
        jsonResponder = signUpRes

    # noinspection PyUnboundLocalVariable
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)


@csrf_exempt
def loginUsers(request):
    if 'loggedin' in request.session:
        if request.session['loggedin']:
            current_user = functions.searchUserByToken(request.session['token'])
            jsonResponder = {"result": False, "code": 405, "desc": 'Already Loggedin',
                             "currentUser": current_user.fName + " " + current_user.lName}
            return JsonResponse(jsonResponder, JSONEncoder, safe=False)
        else:
            return JsonResponse(functions.doLogin(request) , JSONEncoder , safe=False)

    else:
        return JsonResponse(functions.doLogin(request), JSONEncoder, safe=False)


@csrf_exempt
def logOut(request):
    try:
        request.session.flush()
        return JsonResponse({"result": True, "code": 200, "desc": "You have Logged Out Success Fully"}, JSONEncoder)
    except KeyError:
        pass
