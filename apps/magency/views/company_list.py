from core.views import SmartView
from core.views.base import AdminView

__author__ = 'sha256'


class CompanyListView(AdminView):

    def get(self, request):
        return self.render(request, "magency/companies_list.html", {})
