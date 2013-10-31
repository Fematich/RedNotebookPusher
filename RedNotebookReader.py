#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Thu Oct 31 16:58:49 2013
"""
import os
import re
import logging

logger=logging.getLogger('RednotebookReader')
try:
    import yaml
except ImportError:
    logging.error('PyYAML not found. Please install python-yaml or PyYAML')
    sys.exit(1)
    
def getUpdates():
    '''
    checks for updates and returns an iterator over the new entries
    currently only supports checking last day and returning these notes    
    '''

def getNotes(data):
    '''
    given a piece of text it extracts the different entries/notes in it, splitted by a line ------... or =====...
    '''
    # first split different entries
    notes=[]
    # extract the corresponding titles and content 
    # for layout check pango markup.py in rednotebook and form for evernote
    for note in notes:
        title=''
        content=''
        yield title,content
    
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
        
def convert_to_pango(txt, headers=None, options=None):
    '''
    Code partly taken from txt2tags tarball
    '''
    original_txt = txt

    # Here is the marked body text, it must be a list.
    txt = txt.split('\n')

    # Set the three header fields
    if headers is None:
        headers = ['', '', '']

    config = txt2tags.ConfigMaster()._get_defaults()

    config['outfile'] = txt2tags.MODULEOUT  # results as list
    config['target'] = 'xhtml'

    config['preproc'] = []
    # We need to escape the ampersand here, otherwise "&amp;" would become
    # "&amp;amp;"
    config['preproc'].append([r'&amp;', '&'])

    # Allow line breaks
    config['postproc'] = []
    config['postproc'].append([REGEX_LINEBREAK, '\n'])

    if options is not None:
        config.update(options)

    # Let's do the conversion
    try:
        body, toc = txt2tags.convert(txt, config)
        full_doc = body
        finished = txt2tags.finish_him(full_doc, config)
        result = ''.join(finished)

    # Txt2tags error, show the messsage to the user
    except txt2tags.error, msg:
        logging.error(msg)
        result = msg

    # Unknown error, show the traceback to the user
    except:
        result = txt2tags.getUnknownErrorMessage()
        logging.error(result)

    # remove unwanted paragraphs
    result = result.replace('<p>', '').replace('</p>', '')

    logging.log(5, 'Converted "%s" text to "%s" txt2tags markup' %
                (repr(original_txt), repr(result)))

    # Remove unknown tags (<a>)
    def replace_links(match):
        """Return the link name."""
        return match.group(1)
    result = re.sub(REGEX_HTML_LINK, replace_links, result)

    try:
        attr_list, plain, accel = pango.parse_markup(result)

        # result is valid pango markup, return the markup
        return result
    except gobject.GError:
        # There are unknown tags in the markup, return the original text
        logging.debug('There are unknown tags in the markup: %s' % result)
        return original_txt
