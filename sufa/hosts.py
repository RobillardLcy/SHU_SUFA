from django.conf import settings
from apps.administrator import urls
from django_hosts import patterns, host

host_patterns = patterns('',
                         host(r'www', settings.ROOT_URLCONF, name='home'),
                         host(r'admin', urls, name='admin'),
)
