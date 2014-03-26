__author__ = 'sha256'
from django.conf import settings
from django.conf.urls import patterns, include, url
import datetime
import os


def module_exists(module_name):

    try:
        __import__(module_name)
    except ImportError, e:
        return False
    else:
        return True


def handle_uploaded_file(FILE_UPLOAD_DIR, source):
    path = os.path.join(FILE_UPLOAD_DIR, source.name)
    dest = open(path, 'wb')
    if source.multiple_chunks:
        for c in source.chunks():
            dest.write(c)
    else:
        dest.write(file.read())
    dest.close()


def convertDatetimeToString(o, DATE_FORMAT="%Y-%m-%d", TIME_FORMAT="%H:%M:%S"):

    if isinstance(o, datetime.datetime):
        return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
    elif isinstance(o, datetime.date):
        return o.strftime(DATE_FORMAT)
    elif isinstance(o, datetime.time):
        return o.strftime(TIME_FORMAT)


def autourlpatters():

    urlpatterns = patterns('')
    for app in settings.INSTALLED_APPS:
        if not app.startswith("django") and not app.startswith("debug") and module_exists(app + ".urls"):
            foo = app.split(".")[-1]
            urlpatterns += patterns('',
                url(r'^' + foo + '/', include(app+".urls"))
            )
    return urlpatterns
