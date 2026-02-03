from ..models import Reports
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class ReportService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_reports where 1=1"
        val = params.get('reportName', None)
        if (DataValidator.isNotNull(val)):
            sql += " and reportName like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'reportId', 'reportName','generatedDate', 'generatedBy', 'reportStatus')
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
        return Reports