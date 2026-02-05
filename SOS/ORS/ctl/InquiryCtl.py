from Tools.scripts.fixdiv import report

from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..models import Inquiry
from ..utility.DataValidator import DataValidator
from ..service.InquiryService import InquiryService


class InquiryCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id', 0)
        self.form['inquiryId'] = requestForm.get('inquiryId')
        self.form['inquiryName'] = requestForm.get('inquiryName')
        self.form['inquiryDate'] = requestForm.get('inquiryDate')
        self.form['email'] = requestForm.get('email')
        self.form['inquirySubject'] = requestForm.get('inquirySubject')
        self.form['inquiryStatus'] = requestForm.get('inquiryStatus')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.inquiryId = self.form['inquiryId']
        obj.inquiryName = self.form['inquiryName']
        obj.inquiryDate = self.form['inquiryDate']
        obj.email = self.form['email']
        obj.inquirySubject = self.form['inquirySubject']
        obj.inquiryStatus = self.form['inquiryStatus']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['inquiryId'] = obj.inquiryId
        self.form['inquiryName'] = obj.inquiryName
        self.form['inquiryDate'] = obj.inquiryDate
        self.form['email'] = obj.email
        self.form['inquirySubject'] = obj.inquirySubject
        self.form['inquiryStatus'] = obj.inquiryStatus


    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]

        if DataValidator.isNull(self.form['inquiryId']):
            inputError['inquiryId'] = "Inquiry Id can not be null"
            self.form['error'] = True

        if DataValidator.isNull(self.form["inquiryName"]):
            inputError["inquiryName"] = "Inquiry Name is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["inquiryDate"])):
            inputError["inquiryDate"] = "Inquiry Date is required"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form['inquiryDate'])):
                inputError['inquiryDate'] = "Incorrect Date of birth"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["email"])):
            inputError["email"] = "Email ID is required"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form['email'])):
                inputError['email'] = "Email ID must be like student@gmail.com"
                self.form['error'] = True

        if DataValidator.isNull(self.form["inquirySubject"]):
            inputError["inquirySubject"] = "Subject of Inquiry is required"
            self.form["error"] = True

        if DataValidator.isNull(self.form["inquiryStatus"]):
            inputError["inquiryStatus"] = "Inquiry Status is required"
            self.form["error"] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            report = self.get_service().get(params['id'])
            self.model_to_form(report)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(inquiryId=self.form['inquiryId'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Inquiry already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                inquiry= self.form_to_model(Inquiry())
                self.get_service().save(inquiry)
                self.form['id'] = inquiry.id
                self.form['error'] = False
                self.form['message'] = "Inquiry updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:
            duplicate = self.get_service().get_model().objects.filter(inquiryId=self.form['inquiryId'])

            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Inquiry already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                inquiry = self.form_to_model(Inquiry())
                self.get_service().save(inquiry)
                self.form['error'] = False
                self.form['message'] = "Inquiry added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Inquiry.html"

    def get_service(self):
        return InquiryService()