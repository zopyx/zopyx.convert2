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

fop_home = os.environ.get('FOP_HOME')

def _check_fop():
    if not checkEnvironment('FOP_HOME'):
        return False

    exe_name = win32 and 'fop.bat' or 'fop'
    full_exe_name = os.path.join(fop_home, exe_name)
    if not os.path.exists(full_exe_name):
        LOG.debug('%s does not exist' % full_exe_name)
        return False

    return True

def fo2pdf(fo_filename, output_filename=None):
    """ Convert a FO file to PDF using FOP"""

    if not output_filename:
        output_filename = newTempfile(suffix='.pdf')

    if not fop_available:
        raise RuntimeError("The external FOP converter isn't available")

    if sys.platform == 'win32':
        cmd = '%s\\fop.bat -fo "%s" -pdf "%s"' % (fop_home, fo_filename, output_filename)
    else:
        cmd = '%s "%s/fop" -fo "%s" -pdf "%s"' % \
              (execution_shell, fop_home, fo_filename, output_filename)

    status, output = runcmd(cmd)
    if status != 0:
        raise ConversionError('Error executing: %s' % cmd, output)

    return dict(output_filename=output_filename,
                status=status,
                output=output)


class HTML2PDF(BaseConverter):

    name = 'pdf-fop'
    output_format = 'pdf'
    visible_name = 'PDF (FOP)'
    visible = True

    @staticmethod
    def available():
        return fop_available

    def convert(self, output_filename=None, **options):
        options['strip_base'] = True
        self.convert2FO(**options)
        result = fo2pdf(self.fo_filename, output_filename)
        return result

fop_available = _check_fop()

from registry import registerConverter
registerConverter(HTML2PDF)
