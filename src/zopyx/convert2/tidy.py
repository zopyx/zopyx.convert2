##########################################################################
# zopyx.convert2 - SmartPrintNG low-level functionality
#
# (C) 2007, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

import os
import re
import logging

from util import newTempfile
from htmlentitydefs import name2codepoint
from BeautifulSoup import BeautifulSoup

LOG = logging.getLogger('zopyx.convert2')

def tidyhtml(filename, encoding='utf-8', strip_base=False):

    html = file(filename, 'rb').read()

    # use BeautifulSoup for performing HTML checks
    # and conversion to XHTML
    soup = BeautifulSoup(html)

    # check if all image files exist
    for img in soup.findAll('img'):
        src = img['src']
        if not os.path.exists(src):
            # try to find the image relative to the location of
            # the HTML file
            html_dirname = os.path.dirname(filename)
            possible_img = os.path.join(html_dirname, src)
            if os.path.exists(possible_img):
                img['src'] = possible_img
            else:
                LOG.warn('No image file found: %s' % src)

    html = soup.renderContents()

    # replace the HTML tag
    html = '<html xmlns="http://www.w3.org/1999/xhtml">' + \
            html[html.find('<html') + 6:]
    # add the XML preamble
    html = '<?xml version="1.0" ?>\n' + html

    # replace all HTML entities with numeric entities
    def handler(mo):
        """ Callback to convert entities """
        e = mo.group(1)
        v = e[1:-1]
        if not v.startswith('#'):
            codepoint =  name2codepoint.get(v)
            return codepoint and '&#%d;' % codepoint or ''
        else:
            return e
    
    entity_reg = re.compile('(&.*?;)')
    html = entity_reg.sub(handler, html)

    # replace BASE tag
    if strip_base:
        base_reg = re.compile('(<base.*?>)', re.I)
        html = base_reg.sub('', html)

    base, ext = os.path.splitext(filename)
    tidy_filename = '%s-tidy%s' % (base, ext)
    import pdb; pdb.set_trace() 
    file(tidy_filename, 'wb').write(str(html))
    return tidy_filename

