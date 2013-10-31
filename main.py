#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Thu Oct 31 16:38:21 2013
"""

import json
from EvernotePusher import *
from RedNotebookReader import *

    

if __name__ == '__main__':
    try:
        settings=json.load(open('settings.json','r'))
        auth_token=settings['auth_token']
        datadir=settings['datadir']
        NOTEBOOK=settings['NOTEBOOK']
    except Exception:
        #first usage:
        print 'Please provide a complete settingsfile'
        exit(1)
