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

from exceptions import ConversionError
from sx.pisa3.pisa_document import pisaDocument


def html2pdf(html_filename, output_filename=None, **options):
    """ Convert a HTML file to PDF using FOP"""

    if not output_filename:
        output_filename = newTempfile(suffix='.pdf')

    cmd = 'pisa --encoding utf-8 -d "%s" "%s"' % (html_filename, output_filename)
    status, output = runcmd(cmd)
    
    return dict(output_filename=output_filename,
                status=0,
                output=output)


class HTML2PDF(BaseConverter):

    name = 'pdf-pisa-bin'
    output_format = 'pdf'
    visible_name = 'PDF (PISA, binary binary converter)'
    visible = True

    @staticmethod
    def available():
        return True

    def convert(self, output_filename=None, **options):
        result = html2pdf(self.filename, output_filename, **options)
        return result

from registry import registerConverter
registerConverter(HTML2PDF)

