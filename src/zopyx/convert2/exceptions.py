##########################################################################
# zopyx.convert2 - XSL-FO related functionalities
#
# (C) 2007, 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

class ConversionError(Exception):
    """ Generic conversion exception holding and error message
        and the output from the failed conversion.
    """

    def __init__(self, error_msg, output):
        self.error_msg = error_msg
        self.output = output

    def __str__(self):
        return '%s\nOutput:\n%s' % (self.error_msg, self.output)

