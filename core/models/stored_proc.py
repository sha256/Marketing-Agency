import cx_Oracle

__author__ = 'sha256'


from django.db import models
from django.db import connection


class StoredProcModel(models.Model):

    """
    @:param params: list of params
    """
    @staticmethod
    def call_proc(proc_name, params):
        cur = connection.cursor()

        cur.callproc(proc_name, params)
        results = cur.fetchall()
        cur.close()

        return [StoredProcModel(*row) for row in results]

    @staticmethod
    def call_func(proc_name, rettype, params):
        cur = connection.cursor()
        cur = cur.callfunc(proc_name, rettype, params)
        res = cur.fetchall()
        cur.close()
        return res

    class Meta:
        abstract = True