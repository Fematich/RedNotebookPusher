#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Thu Oct 31 16:58:49 2013
"""
import os,sys, datetime
import re
import logging
try:
    import yaml
except ImportError:
    logging.error('PyYAML not found. Please install python-yaml or PyYAML')
    sys.exit(1)

logger=logging.getLogger('RednotebookReader')

#splitblock=re.compile('\n[=-]{20,}\n')
splitblock=re.compile('\n={20,}\n')
titleblock=re.compile('=*(\n)*=+(?P<title>[^=]+)=+\n(?P<content>.*)',re.DOTALL)
tags=set()
  
def getUpdates(datadir):
    '''
    checks for updates and returns an iterator over the new entries
    currently only supports checking last day and returning these notes    
    '''
    dateYesterday=datetime.date.today()#-datetime.timedelta(16)
    mth=Month(dateYesterday.year,dateYesterday.month,datadir)
    return mth[dateYesterday.day]
    
def getNotes(data):
    '''
    given a piece of text it extracts the different entries/notes in it, splitted by a line ------... or =====...
    '''
    # first split different entries
    notes=re.split(splitblock, data)
    # extract the corresponding titles and content 
    for note in notes:
        entry={}
        entry['title']=''
        mtch=re.match(titleblock,note)
        if mtch:
            entry['title']=mtch.group('title')
            entry['content']=mtch.group('content')
            if entry['title'] in tags:
                entry['tags']=entry['title']
        else:
            entry['content']=note
        # for layout check pango markup.py in rednotebook and form for evernote
        if entry['content']!='':
            yield entry
    
class Month():
    '''
    given a month and a year, it defines the Month-object, containing the notes of the different days
    the text of the days can be accessed by eg. 
        december=Month(...)
        december.day[x]['text']
    the notes of the days can be accessed by getitem:
        december=Month(...)
        december[x]
    '''
    def __init__(self,year,month,datadir):
        try:
            with open(os.path.join(datadir,'%d-%d.txt'%(year,month))) as f:
                self.days=yaml.load(f)
        except Exception:
            logger.error('failed to initialize Month')
    
    def __getitem__(self,day):
        try:
            text=self.days[day]['text']
        except KeyError:
            text=''
        return getNotes(text)
        
