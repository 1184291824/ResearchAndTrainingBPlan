from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib.auth import logout
from django.utils import timezone

# Create your views here.


def test(request):
    return HttpResponse('hello world')
