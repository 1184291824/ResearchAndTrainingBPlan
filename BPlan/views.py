from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib.auth import logout
from django.utils import timezone
from .meta import *

# Create your views here.


def test(request):
    login_information = get_agent(request)
    ip = get_ip(request)
    location = get_location(ip)
    return HttpResponse(
        '<h1>browser:' + login_information['browser'] +
        '</h1><h1>system:' + login_information['system'] +
        '</h1><h1>device:' + login_information['device'] +
        '</h1><h1>ip:' + ip +
        '</h1><h1>location:' + location + '</h1>'+
        request.META['HTTP_USER_AGENT']
    )

