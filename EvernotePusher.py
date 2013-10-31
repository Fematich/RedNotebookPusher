#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Thu Oct 31 17:00:29 2013
"""

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import hashlib
import binascii
import logging

logger=logging.getLogger('EvernoteComm')

#authentication
client = EvernoteClient(token=auth_token)
userStore = client.get_user_store()
noteStore = client.get_note_store()


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
    '''
    
def addNote(title,content,notebook=NOTEBOOK):
    '''
    adds a note (title, content) to the standard Notebook
    '''
    noteStore = client.get_note_store()
    note = Types.Note()
    note.title = title
    note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>%s</en-note>'%content
    note = noteStore.createNote(note)
    logger.info('added note:%s, with guid:%s'%(title,str(notebook.guid)))
    return note.guid

def addNotebook(notebookname):
    '''
    adds a Notebook to the noteStore if needed(to store all Rednotebook entries)
    '''
    notebook = Types.Notebook()
    notebook.name = notebookname
    notebook = noteStore.createNotebook(notebook)
    logger.info('added notebook:%s, with guid:%s'%(notebookname,str(notebook.guid)))
    return notebook.guid

def CheckVersion():
    user_store = client.get_user_store()
    version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
    )
    print "Is my Evernote API version up to date? ", str(version_ok)
    print ""
    return version_ok:  