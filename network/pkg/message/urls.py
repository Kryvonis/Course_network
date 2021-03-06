"""network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^datagram$', view=views.send_message_in_datagram, name='datagram'),
    url(r'^connect$', view=views.send_message_in_connect, name='connect'),
    url(r'^run/(?P<type>[0-9A-Za-z]+)$', view=views.run, name='run'),
    url(r'^simul$', view=views.run_simul, name='run-simul'),

]
