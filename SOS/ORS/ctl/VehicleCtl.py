from ..service.CollegeService import CollegeService
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import Vehicle
from..service.VehicleService import VehicleService

class VehicleCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['vehicleName'] = requestForm['vehicleName']
        self.form['vehicleNumber'] = requestForm['vehicleNumber']
        self.form['licenseDate'] = requestForm['licenseDate']
        self.form['vehicleOwner'] = requestForm['vehicleOwner']


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.vehicleName = self.form['vehicleName']
        obj.vehicleNumber = self.form['vehicleNumber']
        obj.licenseDate = self.form['licenseDate']
        obj.vehicleOwner = self.form['vehicleOwner']
        return obj


    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['vehicleName'] = obj.vehicleName
        self.form['vehicleNumber'] = obj.vehicleNumber
        self.form['licenseDate'] = obj.licenseDate.strftime("%Y-%m-%d")
        self.form['vehicleOwner'] = obj.vehicleOwner

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['vehicleName'])):
            inputError['vehicleName'] = "Vehicle Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['vehicleName'])):
                inputError['vehicleName'] = "Vehicle Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['vehicleNumber'])):
            inputError['vehicleNumber'] = "vehicle Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeckroll(self.form['vehicleNumber'])):
                inputError['vehicleNumber'] = "vehicle Number contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['licenseDate'])):
            inputError['licenseDate'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['licenseDate'])):
                inputError['licenseDate'] = "Incorrect Date, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['vehicleOwner'])):
            inputError['vehicleOwner'] = "vehicle Owner can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['vehicleOwner'])):
                inputError['vehicleOwner'] = "vehicle Owner contains only letters"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            vehicle = self.get_service().get(params['id'])
            self.model_to_form(vehicle)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        if (int(self.form['id']) > 0):
            pk = int(self.form['id'])
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(vehicleNumber=self.form['vehicleNumber'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Vehicle already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                vehicle = self.form_to_model(Vehicle())
                self.get_service().save(vehicle)
                self.form['id'] = vehicle.id
                self.form['error'] = False
                self.form['message'] = "Vehicle updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
        else:
            duplicate = self.get_service().get_model().objects.filter(vehicleNumber=self.form['vehicleNumber'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Vehicle already exist"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                vehicle = self.form_to_model(Vehicle())
                self.get_service().save(vehicle)
                self.form['error'] = False
                self.form['message'] = "Vehicle added successfully..!!"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Vehicle.html"

    def get_service(self):
        return VehicleService()