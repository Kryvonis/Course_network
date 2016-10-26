from django.db import models


# Create your models here.
class Node:
    def __init__(self):
        self.id = 0
        self.chanels = []
        self.X = 0
        self.Y = 0

    def __str__(self, *args, **kwargs):
        return "<Node id={0} chanels={1} X={2} Y={3}".format(
            self.id, self.chanels, self.X, self.Y)

    def __repr__(self, *args, **kwargs):
        return "<Node id={0} chanels={1} X={2} Y={3}".format(
            self.id, self.chanels, self.X, self.Y)
