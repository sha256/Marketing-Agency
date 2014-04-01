from datetime import datetime
from apps.magency.rowmapper import RowMapper
from core.views import SmartView, SecuredView

__author__ = 'sha256'

import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


class ReportView(SecuredView):

    def get(self, request):
        data = {}

        return self.render(request, "magency/reports.html", data)


class ReportDownloadView(SecuredView):

    def get(self, request, what):
        data = {}

        idx = 0
        if not request.user.is_staff:
            idx = request.user.id

        if what == "bills":
            data['staff'] = request.user.is_staff
            data['bills'] = RowMapper.call_proc('bills(%s, :curr)' % idx,
                                                      ['id', 'title', 'name', 'ammount', 'paid_by', 'time'])

            data['who'] = request.user.name if not request.user.is_staff else "Marketing Agency"
            data['datetime'] = datetime.now()

            return render_to_pdf("magency/reports_bill.html", data)