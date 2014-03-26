
from django.conf.urls import patterns, url
from apps.magency.views.ajax import AjaxView
from apps.magency.views.company_list import CompanyListView
from apps.magency.views.dashboard import DashboardView
from apps.magency.views.domain import DomainView

urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'companies/$', CompanyListView.as_view(), name="company_list"),
    url(r'domains/(?P<what>([a-z]+))$', DomainView.as_view(), name="domain"),
    url(r'ajax$', AjaxView.as_view(), name="ajax"),

)
