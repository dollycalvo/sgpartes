"""
WSGI config for sgpartes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

path = '/var/www/sgpartes_2'
if path not in sys.path:
   sys.path.append(path)

#os.environ['DJANGO_SETTINGS_MODULE'] = 'sgpartes.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpartes.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


#os.environ['DJANGO_SETTINGS_MODULE'] = 'sgpartes.settings'

#from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgpartes.settings')

#application = get_wsgi_application()