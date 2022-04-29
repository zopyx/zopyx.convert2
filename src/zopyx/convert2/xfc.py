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

xfc_dir = os.environ.get('XFC_DIR')

def _check_xfc():
    if not checkEnvironment('XFC_DIR'):
        return False

    # check only for fo2rtf (we expect that all other fo2XXX
    # converters are also installed properly)
    full_exe_name = os.path.join(xfc_dir, 'fo2rtf')
    if not os.path.exists(full_exe_name):
        LOG.debug(f'{full_exe_name} does not exist')
        return False

    return True


def fo2xfc(fo_filename, format='rtf', output_filename=None):
    """ Convert a FO file to some format support 
        through XFC-4.0.
    """

    if format not in ('rtf', 'docx', 'wml', 'odt'):
        raise ValueError(f'Unsupported format: {format}')

    if not output_filename:
        output_filename = newTempfile(suffix=f'.{format}')

    if sys.platform == 'win32':
        cmd = '"%s\\fo2%s.bat"  "%s" "%s"' % (xfc_dir, format, fo_filename, output_filename) 
    else:	
        cmd = '"%s/fo2%s" "%s" "%s"' % (xfc_dir, format, fo_filename, output_filename)


    status, output = runcmd(cmd)
    if status != 0:
        raise ConversionError(f'Error executing: {cmd}', output)

    return dict(output_filename=output_filename,
                status=status,
                output=output)

class RTFConverter(BaseConverter):

    name = 'rtf-xfc'
    output_format = 'rtf'
    visible_name = 'RTF (XINC)'
    visible = True

    @staticmethod
    def available():
        return xfc_available

    def convert(self, output_filename=None, **options):
        options['strip_base'] = True
        self.convert2FO(**options)
        return fo2xfc(self.fo_filename, self.output_format, output_filename)

class WMLConverter(RTFConverter):

    name = 'wml-xfc'
    output_format = 'wml'
    visible_name = 'WML (XINC)'
    visible = True

class DOCXConverter(RTFConverter):

    name = 'ooxml-xfc'
    output_format = 'docx'
    visible_name = 'OOXML (XINC)'
    visible = True

class ODTConverter(RTFConverter):

    name = 'odt-xfc'
    output_format = 'odt'
    visible_name = 'ODT (XINC)'
    visible = True


xfc_available = _check_xfc()

from registry import registerConverter
registerConverter(RTFConverter)
registerConverter(WMLConverter)
registerConverter(DOCXConverter)
registerConverter(ODTConverter)
