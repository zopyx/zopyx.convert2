##########################################################################
# zopyx.convert2 - SmartPrintNG low-level functionality
#
# (C) 2007, 2008, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

"""
A simple converter registry
"""


# map converter name to converter class
converter_registry = {}

def registerConverter(converter_cls):
    converter_registry[converter_cls.name] = converter_cls


def availableConverters():
    results = [name for name, cls in converter_registry.items() if cls.available()]
    return sorted(results)
