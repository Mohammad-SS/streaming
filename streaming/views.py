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
    data_recived = None
    # First Check if all arguments is passed by POST data .
    if set(['username', 'password', 'fname', 'lname', 'phone', 'numberid', 'birthdate', 'educationlvl']).issubset(request.POST):
        data_recived = {"username": request.POST['username'], "password": request.POST['password'], "fname": request.POST['fname'],
                        "lname": request.POST['lname'], "nid": request.POST['numberid'], "birthdate": request.POST['birthdate'], "edlvl": request.POST['educationlvl'], 'phone': request.POST['phone']}
    else:
        # if its not passed , so give 404 code
        jsonResponder = {"resule": False, "code": 400,
                         "desc": "defective data recived"}

    if(data_recived is not None):
        signUpRes = functions.signUP(data_recived)
        jsonResponder = signUpRes
    return JsonResponse(jsonResponder, JSONEncoder, safe=False)
