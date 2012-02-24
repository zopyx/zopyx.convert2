##########################################################################
# zopyx.convert2 - SmartPrintNG low-level functionality
#
# (C) 2007, 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

import os
import sys

from convert import BaseConverter
from util import runcmd, which, win32, checkEnvironment, newTempfile, execution_shell
from logger import LOG

from tidy import tidyhtml
from exceptions import ConversionError

def _check_pdfreactor():
    if not which('pdfreactor'):
        return False
    return True

pdfreactor_available = _check_pdfreactor()

def html2pdf(html_filename, output_filename=None, **options):
    """ Convert a HTML file to PDF using FOP"""

    if not output_filename:
        output_filename = newTempfile(suffix='.pdf')

    if not pdfreactor_available:
        raise RuntimeError("The external 'pdfreactor' converter isn't available")

    cmd = '%s "pdfreactor" "%s" "%s"' % \
          (execution_shell, html_filename, output_filename)
    
    status, output = runcmd(cmd)
    if status != 0:
        raise ConversionError('Error executing: %s' % cmd, output)
    return dict(output_filename=output_filename,
                status=status,
                output=output)


class HTML2PDF(BaseConverter):

    name = 'pdf-pdfreactor'
    output_format = 'pdf'
    visible_name = 'PDF (pdfreactor)'
    visible = True

    @staticmethod
    def available():
        return pdfreactor_available

    def convert(self, output_filename=None, **options):
        tidy_filename = tidyhtml(self.filename, self.encoding)
        result = html2pdf(tidy_filename, output_filename, **options)
        os.unlink(tidy_filename)
        return result


from registry import registerConverter
registerConverter(HTML2PDF)

if __name__ == '__main__':
    print html2pdf(sys.argv[1], 'out.pdf', **{'encrypt' : None,
                                              'disallow-print' : None,
                                              'disallow-copy' : None,
                                              'disallow-modify' : None,
                                              'owner-password' : 'foo1',
                                              'user-password' : 'foo'})['output_filename']
