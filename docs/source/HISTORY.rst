Changelog
=========

2.4.5 (2012-11-05)
------------------
- fixed typo

2.4.4 (2012-11-05)
------------------
- creating tidyed file inside the existing folder instead
  of in $TMPDIR. This error caused that some style files 
  could not we loaded with PDFreactor

2.4.3 (2012-06-20)
------------------
- fixed logger (mis-)usage
- fixed API documentation 

2.4.2 (2012-01-01)
------------------
- experimental support for PDFreactor

2.4.1 (2011-11-11)
------------------
- fixed BeautifulSoup dependency

2.4 (2011-11-07)
------------------
- documentation updated in order to reflect changes
  to the first public release of the Plone Client Connector

2.3.2 (2011-08-23)
------------------
- added support for %(WORKDIR)s substitution in Calibre converter

2.3.1 (2011-06-15)
------------------
- support for PISA (pdf-pisa-bin) - requires that 'pisa'
  is found in the $PATH
 
2.3.0 (2011-06-05)
------------------
- support for PISA (pdf-pisa)
 
2.2.5 (2011-04-03)
------------------
- calibre converter now honors the commandlineoptions.txt file

2.2.4 (2010-12-16)
------------------
- stripping of BASE tag for XFC-based converters 

2.2.3 (2010-08-16)
------------------
- made stripping of the BASE tag specific to pdf-fop

2.2.2 (2010-08-15)
------------------
- pdf-fop converter not registered properly

2.2.1 (2010-07-19)
------------------
- support $ZOPYX_CONVERT_SHELL 

2.2.0 (2010-05-15)
------------------
- dedicated ConversionError exception added

2.1.1 (2010-02-19)
------------------
- relaxed tidy check for existence of images

2.1.0 (2009-09-05)
------------------
- Calibre integration
- API change: convert() now returns a richer dict with all related
  conversion results

2.0.4 (2009-07-07)
--------------------
- pinned BeautifulSoup 3.0.x

2.0.3 (2009-07-05)
--------------------
- fix in fop.py

2.0.2 (2009-06-02)
--------------------
- fixed broken path for test data files

2.0.1 (2009-06-02)
--------------------
- added environment variable ZOPYX_CONVERT_EXECUTE_METHOD to control the usage
  of the process module vs. os.system() (in case of hanging Java processes).
  Possible values: 'process' (default), 'system'

2.0.0 (2009-05-14)
--------------------
- final release

2.0.0b3 (25.12.2008)
--------------------
- tidy: rewrite image references relative to the html
  file to be converted

2.0.0b2 (05.10.2008)
--------------------
- fixed some import errors
- now working with zopyx.smartprintng.core

2.0.0b1 (04.10.2008)
--------------------
- initial release
- complete new reimplementation of zopyx.convert
- added support for PrinceXML
