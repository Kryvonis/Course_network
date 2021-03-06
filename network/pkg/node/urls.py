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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index-node'),
    url(r'^node/add$', view=views.add_node, name='add-node'),
    url(r'^node/shutdown$', view=views.shutdown_node, name='add-node'),
    url(r'^regenerate$', view=views.regenerate, name='regenerate-node'),
    url(r'^jsonsave$', view=views.save, name='save-node-json'),
    url(r'^load$', view=views.load, name='load-node-json'),
    url(r'^save$', view=views.save_pos, name='save'),
    url(r'^node/remove/(?P<id>[0-9]+)$', view=views.remove_node, name='remove-node'),
    url(r'^node/init/(?P<type>[0-9A-Za-z]+)$', view=views.init_nodes, name='init-node'),

]
