from django.http import HttpResponse
from django.shortcuts import render
from .BaseCtl import BaseCtl


class WelcomeCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['address'] = requestForm['address']
        self.form['state'] = requestForm['state']
        self.form['city'] = requestForm['city']
        self.form['phoneNumber'] = requestForm['phoneNumber']

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if DataValidator.isNull(self.form['name']):
            inputError['name'] = "College Name can not be null"
            self.form['error'] = True

        else:
            if DataValidator.isalphacehck(self.form['name']):
                inputError['name'] = "College Name considers only letters"
                self.form['error'] = True

        if DataValidator.isNull(self.form['address']):
            inputError['address'] = "College Address can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['state'])):
            inputError['state'] = "College State can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['city'])):
            inputError['city'] = "College City can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['phoneNumber'])):
            inputError['phoneNumber'] = "College Phone Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['phoneNumber'])):
                inputError['phoneNumber'] = "Only numbers's allowed which starts with 6,7,8,9"
                self.form['error'] = True

        return self.form['error']




    def display(self, request, params={}):
        return render(request, self.get_template(), {'form': self.form})

    def submit(self, request, params={}):
        return render(request, self.get_template(), {'form': self.form})

    def get_template(self):
        return "Welcome.html"

    def get_service(self):
        pass