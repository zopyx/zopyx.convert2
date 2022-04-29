##########################################################################
# zopyx.convert2 - SmartPrintNG low-level functionality
#
# (C) 2007, 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

import os
import sys

if sys.version_info >= (2,5):
    from xml.etree.ElementTree import ElementTree,parse, tostring
else:
    from elementtree.ElementTree import parse, tostring, SubElement

from config import java
from tidy import tidyhtml
from util import newTempfile, runcmd, which, win32, checkEnvironment, execution_shell
from logger import LOG
from exceptions import ConversionError


dirname = os.path.dirname(__file__)

class HTML2FO(object):

    name = 'fo'
    output_format = 'fo'
    visible_name = 'FO (css2xslfo)'
    visible = False

    @staticmethod
    def available():
        return True

    def convert(self, filename, encoding='utf-8', tidy=True, output_filename=None, **kw):
        """ Convert a HTML file stored as 'filename' to
            FO using CSS2XSLFO.
        """

        if tidy:
            filename = tidyhtml(filename, encoding, strip_base=kw.get('strip_base', False))

        fo_filename = output_filename or newTempfile(suffix='.fo')
        csstoxslfo = os.path.abspath(os.path.join(dirname, 'lib', 'csstoxslfo', 'css2xslfo.jar'))
        if not os.path.exists(csstoxslfo):
            raise IOError(f'{csstoxslfo} does not exist')

        cmd = '"%s"' % java + \
              ' -Duser.language=en -Xms256m -Xmx256m -jar "%(csstoxslfo)s" "%(filename)s" -fo "%(fo_filename)s"' % vars()
        for k in kw:
            cmd += ' %s="%s"' % (k, kw[k])

        status, output = runcmd(cmd)
        if status != 0:
            raise ConversionError(f'Error executing: {cmd}', output)

        # remove tidy-ed file
        if tidy:
            os.unlink(filename)

        # remove some stuff from the generated FO file causing
        # some conversion trouble either with XINC or XFC

        E = parse(fo_filename)

        ids_seen = []
        for node in E.getiterator():
            get = node.attrib.get

            # ensure that ID attributes are unique
            node_id = get('id')
            if node_id is not None:
                if node_id in ids_seen:
                    del node.attrib['id']
                ids_seen.append(node_id)

            for k, v in (('footnote', 'reset'), 
                         ('unicode-bidi', 'embed'), 
                         ('writing-mode', 'lr-tb'), 
                         ('font-selection-strategy', 'character-by-character'), 
                         ('line-height-shift-adjustment', 'disregard-shifts'), 
                         ('page-break-after', 'avoid'), 
                         ('page-break-before', 'avoid'), 
                         ('page-break-inside', 'avoid')):

                value = get(k)
                if value == v:
                    del node.attrib[k]

            for attr in ('margin-left', 'margin-right', 'margin-top', 'margin-bottom',
                         'padding-left', 'padding-right', 'padding-top', 'padding-bottom'):

                value = get(attr)
                if value == '0':
                    node.attrib[attr] = '0em'

            if get('page-break-after') == 'always':
                del node.attrib['page-break-after']
                node.attrib['break-after'] = 'page'

            if get('text-transform'):
                del node.attrib['text-transform']

            value = get('white-space')
            if value == 'pre':
                del node.attrib['white-space']
                node.text = '\n' + node.text.lstrip()
                for k,v in  {'white-space-treatment' : 'preserve',
                             'white-space-collapse' : 'false',
                             'wrap-option' : 'no-wrap',
                             'linefeed-treatment' : 'preserve' }.items():
                    node.attrib[k] = v

        fo_text = tostring(E.getroot())
        fo_text = fo_text.replace('<ns0:block ' , '<ns0:block margin-top="0" margin-bottom="0" ')  # avoid a linebreak through <li><p> (XFC)
#        fo_text = fo_text.replace('<ns0:block/>', '') # causes a crash with XINC    
        fo_text = fo_text.replace('<ns0:block margin-top="0" margin-bottom="0" />', '') 

        file(fo_filename, 'wb').write(fo_text)
        return fo_filename

from registry import registerConverter
registerConverter(HTML2FO)
