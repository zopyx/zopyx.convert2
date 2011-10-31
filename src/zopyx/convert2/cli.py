##########################################################################
# zopyx.convert2 - SmartPrintNG low-level functionality
#
# (C) 2007, 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################


import sys
import tempfile
from optparse import OptionParser
from convert import Converter
from util import newTempfile

import fo
import fop
import xinc
import xfc
import prince
import registry 

def convert(options, args):

    if options.test_mode:

        import pkg_resources
        print 'Entering testmode'

        for fn in ('test1.html', 'test2.html', 'test3.html'):
            tmpf = newTempfile()
            print fn
            print '-'*len(fn)
            file(tmpf + '.html', 'wb').write(pkg_resources.resource_string('zopyx.convert2.tests.data', fn))

            for name in registry.availableConverters():
                cls = registry.converter_registry[name]
                print '%s: %s.html -> %s.%s' % (name, tmpf, tmpf, cls.output_format)
                C = Converter(tmpf + '.html', verbose=True)
                try:
                    result = C(name, output_filename=tmpf + '.' + cls.output_format)
                    print result
                except Exception, e:
                    print 'FAILED (%s)' % e

            print

    elif options.show_converters:
        print 'Available converters: %s' % ', '.join(registry.availableConverters())
    else:

        for fn in args:
            C = Converter(fn, verbose=options.verbose)
            result = C(options.format, 
                                output_filename=options.output_filename)
            print 'Generated file: %s' % result['output_filename']
   

def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False, help='verbose on')
    parser.add_option('-f', '--format', dest='format',
                      help='|'.join(registry.availableConverters()))
    parser.add_option('-l', '--list-converters', action='store_true', dest='show_converters',
                      default=False, help='show all available converters')
    parser.add_option('-o', '--output', dest='output_filename',
                      help='output filename')
    parser.add_option('-t', '--test', dest='test_mode', action='store_true',
                      help='test converters')
    (options, args) = parser.parse_args()
    if not args and not options.test_mode:
        parser.print_help()
        sys.exit(1)
    convert(options, args)

if __name__ == '__main__':
    main()
