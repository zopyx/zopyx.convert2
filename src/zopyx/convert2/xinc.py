##########################################################################
# zopyx.convert - SmartPrintNG low-level functionality
#
# (C) 2007, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

import os
import sys

from convert import BaseConverter
from util import runcmd, which, win32, checkEnvironment, newTempfile
from logger import LOG

from exceptions import ConversionError

xinc_home = os.environ.get('XINC_HOME')

def _check_xinc():
    if not checkEnvironment('XINC_HOME'):
        return False

    exe_name = win32 and '\\bin\\windows\\xinc.exe' or 'bin/unix/xinc'
    full_exe_name = os.path.join(xinc_home, exe_name)
    if not os.path.exists(full_exe_name):
        LOG.debug('%s does not exist' % full_exe_name)
        return False

    return True

def fo2pdf(fo_filename, output_filename=None):
    """ Convert a FO file to PDF using XINC """

    if not output_filename:
        output_filename = newTempfile(suffix='.pdf')

    if not xinc_available:
        raise RuntimeError("The external XINC converter isn't available")

    if sys.platform == 'win32':
        cmd = '%s\\bin\\windows\\xinc.exe -fo "%s" -pdf "%s"' % (xinc_home, fo_filename, output_filename)
    else:
        cmd = '"%s/bin/unix/xinc" -fo "%s" -pdf "%s"' % (xinc_home, fo_filename, output_filename)

    status, output = runcmd(cmd)
    if status != 0:
        raise ConversionError('Error executing: %s' % cmd, output)
    return dict(output_filename=output_filename,
                status=status,
                output=output)



class HTML2PDF(BaseConverter):

    name = 'pdf-xinc'
    output_format = 'pdf'
    visible_name = 'PDF (XINC)'
    visible = True

    @staticmethod
    def available():
        return xinc_available

    def convert(self, output_filename=None, **options):
        self.convert2FO(**options)
        result = fo2pdf(self.fo_filename, output_filename)
        return result


xinc_available = _check_xinc()

from registry import registerConverter
registerConverter(HTML2PDF)
