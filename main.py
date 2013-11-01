#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Thu Oct 31 16:38:21 2013
"""

import json
from EvernotePusher import *
from RedNotebookReader import *
import logging
    
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')

if __name__ == '__main__':
    logger=logging.getLogger('main')    
    try:
        settings=json.load(open('/home/mfeys/play/RedNotebookPusher/settings.json','r'))
        auth_token=settings['auth_token']
        datadir=settings['datadir']
        NOTEBOOK=settings['NOTEBOOK']
    except Exception:
        #first usage:
        print 'Welcome!\nSince this is the first usage of this tool, you need to answer some questions:'
        settings={}        
        settings['auth_token'] = raw_input("Please enter the aut_token: ")
        settings['datadir'] = raw_input("Please enter the rednotebook data-directory: ")
        notebookname = raw_input("Please enter the name of the notebook to be created: ")
        ENotebook=Evernote(settings['auth_token'],'')
        settings['NOTEBOOK']=ENotebook.addNotebook(notebookname)
        json.dump(settings,open('settings.json','w'))
        print 'All done!!!\nPlease restart the application'
        exit(1)
   
    ENotebook=Evernote(auth_token,NOTEBOOK)
    for entry in getUpdates(datadir):
        print entry
        ENotebook.addNote(entry)
