

TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


# JINGO_INCLUDE_PATTERN = r'\.jinja2'  # use any regular expression here

JINGO_EXCLUDE_APPS = ('debug_toolbar',)


JINJA_CONFIG = {
    'autoescape': False,
    'extensions': ['jinja2.ext.with_',]
}

