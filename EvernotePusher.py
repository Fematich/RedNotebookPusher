#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Thu Oct 31 17:00:29 2013
"""

from evernote.api.client import EvernoteClient
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import hashlib
import binascii
import logging
import re

logger=logging.getLogger('EvernoteComm')

listterm=re.compile("^ *(\-) (?P<item>.*)")
strongterm=re.compile("[=\*]+(?P<text>[^=]+)[=\*]+")
itterm=re.compile("//(?P<text>.*)//")
lineterm=re.compile('-{20,}')
line='<div><hr /></div>'

def transformImage(path):
    '''
    returns the encoded image and the resource information
    '''
    image = open(path, 'rb').read()
    md5 = hashlib.md5()
    md5.update(image)
    hash = md5.digest()

    data = Types.Data()
    data.size = len(image)
    data.bodyHash = hash
    data.body = image

    resource = Types.Resource()
    resource.mime = 'image/png'
    resource.data = data
    hash_hex = binascii.hexlify(hash)
    return '<en-media type="image/png" hash="' + hash_hex + '"/>',resource

def transformContent(content):
    '''
    makes a more ENML like representation, based on <div> blocks
    '''
    notetext=''
    lbuffer=[]
    lines=content.split('\n')
    for line in lines:
        lstmtch=re.match(listterm,line)
        if lstmtch:
            lbuffer.append(lstmtch.group('item'))
        else:
            if lbuffer!=[]:
                notetext+=transformlist(lbuffer)
                lbuffer=[]
            strngmtch=re.match(strongterm,line)
            if strngmtch:
                notetext+=Strong(strngmtch.group('text'))
            else:
                itmtch=re.match(itterm,line)
                if itmtch:
                    notetext+=Italic(itmtch.group('text'))
                else:
                    lnmtch=re.match(lineterm,line)
                    if lnmtch:
                        notetext+=line
                    else:
                        notetext+='<div>%s</div>'%line
    if lbuffer!=[]:
        notetext+=transformlist(lbuffer)
    return notetext


def transformlist(lst):
    ret='<div><ul>'
    for it in lst:
        ret+='<li>'+str(it)+'</li>'
    ret+='</ul></div>'
    return ret
def Strong(text):
    ret='<div><strong>%s</strong></div>'%text
    return ret
def Italic(text):
    ret='<div><em>%s</em></div>'%text
    return ret
class Evernote():
    logger=logging.getLogger('Evernote')
    def __init__(self,auth_token,NOTEBOOK):
        #authentication
        self.client = EvernoteClient(token=auth_token, sandbox=False)
        self.userStore = self.client.get_user_store()
        self.noteStore = self.client.get_note_store()
        self.NOTEBOOK=NOTEBOOK
        self.tags=self.noteStore.listTags()
   
    def addNote(self,entry,notebook=None):
        '''
        adds a note (title, content) to the standard Notebook
        '''
        if notebook==None:
            notebook=self.NOTEBOOK
        note = Types.Note()
        note.notebookGuid=notebook
        note.title = entry['title'].replace(' ','')
        if note.title=='':
            note.title='RedNotebookEntry'
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>%s</en-note>'%transformContent(entry['content'])
        note = self.noteStore.createNote(note)
        logger.info('added note:%s, with guid:%s'%(entry['title'],str(note.guid)))
        return note.guid
    
    def addNotebook(self,notebookname):
        '''
        adds a Notebook to the noteStore if needed(to store all Rednotebook entries)
        '''
        notebook = Types.Notebook()
        notebook.name = notebookname
        notebook = self.noteStore.createNotebook(notebook)
        logger.info('added notebook:%s, with guid:%s'%(notebookname,str(notebook.guid)))
        return notebook.guid
    
    def CheckVersion(self):
        version_ok = self.user_store.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
        )
        print "Is my Evernote API version up to date? ", str(version_ok)
        print ""
        return version_ok