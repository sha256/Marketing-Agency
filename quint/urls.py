from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from quint.settings import STATIC_ROOT, STATIC_URL, MEDIA_ROOT, MEDIA_URL, DEBUG
from django.views.static import serve

urlpatterns = patterns('',
    url(r'^', include('apps.auth.urls')),
    url(r'^', include('apps.magency.urls')),
)

# url pattern for static files
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT, show_indexes=DEBUG)

# url for uploaded media files
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT, show_indexes=DEBUG)
