__author__ = 'sha256'

from core.views import SmartView, SecuredView
from core.utils import log
from django.http import HttpResponse
from apps.securedl.session import add_session
from apps.securedl.models import SecuredFile
#from django.db.models.loading import AppCache


class TestView(SmartView):

    def get(self, request):
        #file = SecuredFile.objects.get(pk=1)
        #add_session(file, 100)
        #fo = AppCache()
        #print fo.get_models('django.contrib.auth.models')

        return HttpResponse("hey")



