#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Thu Oct 31 16:38:45 2013
"""

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
#authentication
dev_token = "S=s1:U=89fd3:E=14966d686b7:C=1420f255aba:P=1cd:A=en-devtoken:V=2:H=495bbd7645454a8d3c93266b4511b328"
client = EvernoteClient(token=dev_token)

#userStore
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

#noteStore
noteStore = client.get_note_store()
notebooks = noteStore.listNotebooks()
for n in notebooks:
    print n.name

noteStore = client.get_note_store()
note = Types.Note()
note.title = "I'm a test note!"
note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>Hello, world!</en-note>'
note = noteStore.createNote(note)