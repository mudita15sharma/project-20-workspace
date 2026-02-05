from ..models import Attendance
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class AttendanceService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_attendance where 1=1"
        val = params.get('attendanceId', None)
        if (DataValidator.isNotNull(val)):
            sql += " and attendanceId like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'attendanceId', 'personName', 'attendanceDate', 'attendanceStatus', 'remarks')
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
        return Attendance