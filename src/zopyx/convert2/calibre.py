##########################################################################
# zopyx.convert2 - SmartPrintNG low-level functionality
#
# (C) 2007, 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

import os
import sys
import shutil

from convert import BaseConverter
from util import runcmd, which, win32, checkEnvironment, newTempfile
from logger import LOG
from exceptions import ConversionError

from tidy import tidyhtml

def _check_calibre():
    if not which('ebook-convert'):
        return False
    return True

calibre_available = _check_calibre()

def html2calibre(html_filename, output_filename=None, cmdopts='', **calibre_options):
    """ Convert a HTML file using calibre """
    
    if not html_filename.endswith('.html'):
        shutil.copy(html_filename, html_filename + '.html')
        html_filename += '.html'

    if not output_filename:
        output_filename = newTempfile(suffix='.epub')

    if not calibre_available:
        raise RuntimeError("The external calibre converter isn't available")

    options = list()
    for k,v in calibre_options.items():
        if v is None:
            options.append('--%s ' % k)
        else:
            options.append('--%s="%s" ' % (k, v)) 

    if sys.platform == 'win32':
        raise NotImplementedError('No support for using Calibre on Windows available')
    else:
        options = ' '.join(options)
        options = options + ' ' + cmdopts
        cmd = '"ebook-convert" "%s" "%s" %s' % (html_filename, output_filename, options)
    
    status, output = runcmd(cmd)
    if status != 0:
        raise ConversionError('Error executing: %s' % cmd, output)

    return dict(output_filename=output_filename,
                status=status,
                output=output)


class HTML2Calibre(BaseConverter):

    name = 'ebook-calibre'
    output_format = 'epub'
    visible_name = 'EPUB (Calibre)'
    visible = True

    @staticmethod
    def available():
        return calibre_available

    def convert(self, output_filename=None, **calibre_options):

        # check for commandlineoptions.txt file
        cmdopts = '' 
        cmdopts_filename = os.path.join(os.path.dirname(self.filename), 'commandlineoptions.txt')
        if os.path.exists(cmdopts_filename):
            cmdopts = file(cmdopts_filename).read()
            cmdopts = cmdopts % dict(WORKDIR=os.path.dirname(self.filename))

        tidy_filename = tidyhtml(self.filename, self.encoding)
        result = html2calibre(tidy_filename, output_filename, cmdopts=cmdopts, **calibre_options)
        os.unlink(tidy_filename)
        return result


from registry import registerConverter
registerConverter(HTML2Calibre)

if __name__ == '__main__':
    print html2calibre(sys.argv[1], 'output.epub')
