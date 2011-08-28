#!/usr/bin/python

from rctk.sessions import Session, SpawnedSession, Manager
from rctk.webpy import app
import os

startupdir = os.getcwd()
manager = None

def application(environ, start_response):
    global manager
    if manager is None:
        classid = environ.get('rctk.classid')
        debug = environ.get('rctk.debug', "false").lower() in ("1", "true")
        session = environ.get('rctk.session')
        frontendclass = environ.get('rctk.frontend')
        
        options = {}

        optionconfig = environ.get('options')
        if optionconfig:
            for kv in optionconfig.split(','):
                k, v = kv.split("=", 1)
                options[k] = v
            
        if session == "SpawnedSession":
            sessionclass = SpawnedSession
        else:
            sessionclass = Session

        manager = Manager(sessionclass, classid, frontendclass=frontendclass, debug=debug, **options)
    return app(manager).wsgifunc()(environ, start_response)

