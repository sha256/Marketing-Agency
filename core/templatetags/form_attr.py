__author__ = 'sha256'

from django import template

register = template.Library()

filters = ('size', 'class', "id", "placeholder", "type")
#
# for f in filters:
#     exec('def filter_' + f + '(value, val):\n' +
#             '\tvalue.field.widget.attrs["'+f+'"] = val\n'+
#             '\treturn value')
#     exec('register.filter("' + f + '", filter_' + f + ')')


def filtering(name):

    def fulter(inp, param):
        inp.field.widget.attrs[name] = param
        return inp

    return fulter

for f in filters:
    register.filter(f, filtering(f))


@register.filter
def to_class_name(value):
    return value.__class__.__name__