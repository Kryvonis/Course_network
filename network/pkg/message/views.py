from django.shortcuts import render
from django.http.response import HttpResponse


# Create your views here.

def send_message_in_datagram(request):
    return HttpResponse(200)


def send_message_in_connect(request):
    return HttpResponse(200)
