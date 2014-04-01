from core.views import SmartView, SecuredView

__author__ = 'sha256'


class DashboardView(SecuredView):

    def get(self, request):
        return self.render(request, "magency/dashboard.html", {})
