zopyx.convert2
==============

The ``zopyx.convert2`` package helps you to convert HTML to PDF, RTF, ODT, DOCX
and WML using XSL-FO technology or using PrinceXML. This package is used as the
low-level API for zopyx.smartprintng.core.


Requirements
------------

- Java 1.5.0 or higher (FOP 0.94 requires Java 1.6 or higher)

- `csstoxslfo`__ (included)

__ http://www.re.be/css2xslfo

- `XFC-4.0`__ (XMLMind) for ODT, RTF, DOCX and WML support (if needed)

__ http://www.xmlmind.com/foconverter

- `XINC 2.0`__ (Lunasil) for PDF support (commercial)

__ http://www.lunasil.com/products.html

- or `FOP 0.94`__ (Apache project) for PDF support (free)

__ http://xmlgraphics.apache.org/fop/download.html#dist-type                                            

- or `PrinceXML`__ (commercial) for PDF support 

__ http://www.princexml.com

Installation
------------

- install ``zopyx.convert2`` either using ``easy_install`` or by downloading the sources from the Python Cheeseshop. 
  This will install automatically the Beautifulsoup and Elementree modules if necessary.
- the environment variable *$XFC_DIR* must be set and point to the root of your XFC installation directory
- the environment variable *$XINC_HOME* must be set and to point to the root of your XINC installation directory
- the environment variable *$FOP_HOME* must be set and point to the root of your FOP installation directory
- the 'prince' binary must be in the $PATH if you are using PrinceXML

Supported platforms
-------------------

Windows, Unix


Source code
-----------

- https://github.com/zopyx/zopyx.convert2

Bug tracker
-----------

- https://github.com/zopyx/zopyx.convert2/issues

Usage
-----

Some examples from the Python command-line::

  from zopyx.convert2 import Converter
  C = Converter('/path/to/some/file.html')
  pdf_filename = C('pdf-xinc')       # using XINC
  pdf2_filename = C('pdf-pisa')      # using PISA
  pdf3_filename = C('pdf-fop')       # using FOP
  pdf4_filename = C('pdf-prince')    # using FOP
  rtf_filename = C('rtf-xfc')        
  pdt_filename = C('odt-xfc')
  wml_filename = C('wml-xfc')
  docx_filename = C('docx-xfc')

A very simple command-line converter is also available::

  html-convert --format rtf --output foo.rtf sample.html


`html-convert` has a --test option that will convert some
sample HTML. If everything is ok then you should see something like that::

  >html-convert --test
  Entering testmode
  pdf: /tmp/tmpuOb37m.html -> /tmp/tmpuOb37m.pdf
  rtf: /tmp/tmpuOb37m.html -> /tmp/tmpuOb37m.rtf
  docx: /tmp/tmpuOb37m.html -> /tmp/tmpuOb37m.docx
  odt: /tmp/tmpuOb37m.html -> /tmp/tmpuOb37m.odt
  wml: /tmp/tmpuOb37m.html -> /tmp/tmpuOb37m.wml
  pdf: /tmp/tmpZ6PGo9.html -> /tmp/tmpZ6PGo9.pdf
  rtf: /tmp/tmpZ6PGo9.html -> /tmp/tmpZ6PGo9.rtf
  docx: /tmp/tmpZ6PGo9.html -> /tmp/tmpZ6PGo9.docx
  odt: /tmp/tmpZ6PGo9.html -> /tmp/tmpZ6PGo9.odt
  wml: /tmp/tmpZ6PGo9.html -> /tmp/tmpZ6PGo9.wml


How zopyx.convert2 works internally
-----------------------------------

- The source HTML file is converted to XHTML using mxTidy
- the XHTML file is converted to FO using the great "csstoxslfo" converter
  written by Werner Donne.
- the FO file is passed either to the external XINC or XFC converter to 
  generated the desired output format
- all converters are based on Java technology make the conversion solution
  highly portable across operating system (including Windows)

Environment variables
---------------------

The following environment variables can be used to resolve OS or distribution
specific problems:

``ZOPYX_CONVERT_SHELL`` - defaults to ``sh`` and is used to as shell command to
execute external converters

``ZOPYX_CONVERT_EXECUTION_MODE`` - default to ``process`` and refers to the
method of Python executing external command (by default using the ``process`` module.
Other value: ``system``, ``commands``


Known issues
------------

- If you are using zopyx.convert2 together with FOP: use the latest FOP 0.94
  only.  Don't use any packaged FOP version like the one from MacPorts which is
  known to be broken.    

- Ensure that you have read the ``csstoxslfo`` documentation. ``csstoxslfo`` has
  several requirements about the HTML markup. Don't expect that it is the ultimate
  HTML converter. Any questions regarding the necessary markup are documented in the 
  ``csstoxslfo`` documentation and will not be answered. 

Author
------

``zopyx.convert2`` was written by Andreas Jung for ZOPYX Ltd., Tuebingen, Germany.


License
-------

``zopyx.convert2`` is published under the Zope Public License (ZPL 2.1).
See LICENSE.txt.


Contact
-------

| ZOPYX Ltd.
| Charlottenstr. 37/1
| D-72070 Tuebingen, Germany
| info@zopyx.com
| www.zopyx.com
