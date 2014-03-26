from core.views import SmartView

__author__ = 'sha256'


class DashboardView(SmartView):

    def get(self, request):
        return self.render(request, "magency/dashboard.html", {})
