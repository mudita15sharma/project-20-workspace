from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ..models import Vehicle
from ..service.VehicleService import VehicleService


class VehicleListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['VehicleNumber'] = requestForm.get('VehicleNumber', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        VehicleListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Vehicle.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        VehicleListCtl.count += 1
        self.form['pageNo'] = VehicleListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Vehicle.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        VehicleListCtl.count -= 1
        self.form['pageNo'] = VehicleListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def submit(self, request, params={}):
        VehicleListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['error'] = True
            self.form['message'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/Vehicle/")
        return res

    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                role = self.get_service().get(id)
                if role:
                    self.get_service().delete(id)
                    self.form['error'] = False
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Vehicle.objects.last().id
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def get_template(self):
        return "VehicleList.html"

    def get_service(self):
        return VehicleService()