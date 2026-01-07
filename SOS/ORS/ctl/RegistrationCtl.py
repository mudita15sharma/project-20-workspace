from django.shortcuts import render
from .BaseCtl import BaseCtl
from ..service.UserService import UserService


class RegistrationCtl(BaseCtl):

    def display(self, request, params={}):
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def get_template(self):
        return "Registration.html"

    def get_service(self):
        return UserService()