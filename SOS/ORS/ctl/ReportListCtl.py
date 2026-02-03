from django.shortcuts import render, redirect
from .BaseCtl import BaseCtl
from ..models import Reports
from ..service.ReportService import ReportService


class ReportListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['reportName'] = requestForm['reportName']
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        ReportListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Reports.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        ReportListCtl.count += 1
        self.form['pageNo'] = ReportListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Reports.objects.last().id
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def previous(self, request, params={}):
        ReportListCtl.count -= 1
        self.form['pageNo'] = ReportListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/Report/")
        return res

    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                report = self.get_service().get(id)
                if report:
                    self.get_service().delete(id)
                    self.form['error'] = False
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Reports.objects.last().id
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def submit(self, request, params={}):
        ReportListCtl.count = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        if self.page_list == []:
            self.form['error'] = True
            self.form['message'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "ReportList.html"

    def get_service(self):
        return ReportService()