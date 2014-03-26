from core.views import SmartView

__author__ = 'sha256'


class CompanyListView(SmartView):

    def get(self, request):
        return self.render(request, "magency/companies_list.html", {})
