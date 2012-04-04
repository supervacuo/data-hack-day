"""
WSGI config for youtubeparty project.

"""
import os, sys
import site

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtubeparty.settings")

# Remember original sys.path.
prev_sys_path = list(sys.path) 

site.addsitedir('/usr/local/pythonenv/youtubeparty/lib/python2.6/site-packages/')

# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
        if item not in prev_sys_path:
                new_sys_path.append(item)
                sys.path.remove(item)

sys.path[:0] = new_sys_path 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
