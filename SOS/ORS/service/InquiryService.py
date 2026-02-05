from ..models import Inquiry
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class InquiryService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_inquiry where 1=1"
        val = params.get('inquiryId', None)
        if (DataValidator.isNotNull(val)):
            sql += " and inquiryId like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'inquiryId', 'inquiryName','inquiryDate', 'email','inquirySubject', 'inquiryStatus')
        res = {
            "data": [],
        }
        params["index"] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Inquiry