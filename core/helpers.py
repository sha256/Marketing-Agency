__author__ = 'sha256'

from jingo import register
from .templatetags.form_attr import filtering, filters

for f in filters:
    register.filter(f, filtering(f))