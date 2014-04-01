__author__ = 'sha256'

from django.db import connection
import cx_Oracle

conn = cx_Oracle.connect("system/123@XE")


class RowMapper(object):

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])


    @staticmethod
    def call_func(proc_name, rettype, params):
        cur = connection.cursor()
        cur = cur.callfunc(proc_name, rettype, params)
        res = cur.fetchall()
        cur.close()
        return [RowMapper(dict(zip(['title', 'validity'], row))) for row in res]

    @staticmethod
    def call_proc(proc_name, params):

        cur = conn.cursor()
        outcur = conn.cursor()
        cur.execute("BEGIN %s; END;" % proc_name, curr=outcur)

        res = outcur.fetchall()
        cur.close()
        outcur.close()
        return [RowMapper(dict(zip(params, row))) for row in res]