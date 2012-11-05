##########################################################################
# zopyx.convert2 - SmartPrintNG low-level functionality
#
# (C) 2007, 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

import os

from fo import HTML2FO
import registry

class Converter(object):

    def __init__(self, filename, encoding='utf-8', cleanup=False, verbose=False):
        self.filename = filename
        self.encoding = encoding
        self.cleanup = cleanup
        self.verbose = verbose

    def convert(self, format, output_filename=None, options={}):

        converter = registry.converter_registry.get(format)
        if converter is None:
            raise ValueError('Unsupported format: %s' % format)

        if format == 'fo':
            c = converter()
            output_filename = c.convert(self.filename, 
                                        output_filename=output_filename,
                                        encoding=self.encoding)
        else:
            c = converter(self.filename, self.encoding, self.cleanup, self.verbose)
            output_filename = c.convert(output_filename, **options)
        return output_filename

    __call__ = convert


class BaseConverter(object):
    """High-level OO interface to XSL-FO conversions """


    def __init__(self, filename, encoding='utf-8', cleanup=False, verbose=False):
        self.filename = filename
        self.encoding = encoding
        self.fo_filename = None        
        self.cleanup = cleanup
        self.verbose = verbose

    def convert2FO(self, **options):
        """ Conversion phase 1: HTML -> FO """
        self.fo_filename = HTML2FO().convert(self.filename, self.encoding, **options)

    def convert(self, format, output_filename=None, **options):
        """ 'options' is passwd down html2fo() """

        raise NotImplementedError('convert() must be implemented within a concrete subclass')

    __call__ = convert

    def __del__(self):
        """ House-keeping """

        if self.cleanup:
            if self.fo_filename:
                os.unlink(self.fo_filename)

