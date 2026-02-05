from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import Attendance
from ..service.AttendanceService import AttendanceService


class AttendanceCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['attendanceId'] = requestForm['attendanceId']
        self.form['personName'] = requestForm['personName']
        self.form['attendanceDate'] = requestForm['attendanceDate']
        self.form['attendanceStatus'] = requestForm['attendanceStatus']
        self.form['remarks'] = requestForm['remarks']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.attendanceId = self.form['attendanceId']
        obj.personName = self.form['personName']
        obj.attendanceDate = self.form['attendanceDate']
        obj.attendanceStatus = self.form['attendanceStatus']
        obj.remarks = self.form['remarks']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['attendanceId'] = obj.attendanceId
        self.form['personName'] = obj.personName
        self.form['attendanceDate'] = obj.attendanceDate.strftime("%Y-%m-%d")
        self.form['attendanceStatus'] = obj.attendanceStatus

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['attendanceId'])):
            inputError['attendanceId'] = "Attendance Id can not be null. "
            self.form['error'] = True

        if (DataValidator.isNull(self.form['personName'])):
            inputError['personName'] = "Person Name  can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['personName'])):
                inputError['personName'] = "Person Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['attendanceDate'])):
            inputError['attendanceDate'] = "Attendance Date can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['attendanceDate'])):
                inputError['attendanceDate'] = "Incorrect Date, should be YYYY-MM-DD"
                self.form['error'] = True

        if DataValidator.isNull(self.form["attendanceStatus"]):
            inputError["attendanceStatus"] = "Attendance Status is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form['remarks'])):
            inputError['remarks'] = "Remarks  can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['remarks'])):
                inputError['remarks'] = "Remarks contains only letters"
                self.form['error'] = True

        return self.form['error']


    def display(self, request, params={}):
        if (params['id'] > 0):
            attendance = self.get_service().get(params['id'])
            self.model_to_form(attendance)
        res = render(request, self.get_template(), {"form": self.form})
        return res


    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(attendanceId=self.form['attendanceId'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Attendance Id already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                attendance = self.form_to_model(Attendance())
                self.get_service().save(attendance)
                self.form['id'] = attendance.id
                self.form['error'] = False
                self.form['message'] = "Attendance updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:
            duplicate = self.get_service().get_model().objects.filter(attendanceId=self.form['attendanceId'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Attendance Id already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                attendance = self.form_to_model(Attendance())
                self.get_service().save(attendance)
                self.form['error'] = False
                self.form['message'] = "Attendance added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res


    def get_template(self):
        return "attendance.html"


    def get_service(self):
        return AttendanceService()
