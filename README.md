RedNotebookPusher
=================

Reads Rednotebook entries (multiple entries per day) and pushes them to Evernote

TODO
=================
- currently only checks the entries from yesterday and pushes these to evernote
 - idea is to keep a local version so that all notes can be updated (full Evernote API needed to change notes)
- the parser assumes the complete line is cursive or bold, only the bold/cursive words in the special sentence will be added to evernote
