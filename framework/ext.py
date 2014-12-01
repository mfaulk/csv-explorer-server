'''
Framework utilities for extensions
'''

import imp
import os
import inspect
import sys
from factors.nodes import FactorNode

# From a backport of importlib
def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


# From a backport of importlib
def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]


def package_contents(package_name):
    '''
    List all modules in a package
    :param package_name: Python package
    :return: List[String] of module names
    '''
    file, pathname, description = imp.find_module(package_name)

    if file:
       raise ImportError('Not a package: %r', package_name)
    MODULE_EXTENSIONS = ('.py')
    modules = set([os.path.splitext(module)[0]
       for module in os.listdir(pathname)
       if module.endswith(MODULE_EXTENSIONS)])
    return modules, pathname


def subclasses_in_module(base_class, module):
    '''
    Get subclasses of FactorNode defined in a module

    :param module: a python module object
    :return: Set of class names
    '''
    # class_names = set()
    # for name, obj in inspect.getmembers(sys.modules[module_name]):
    #     print name
    #     if inspect.isclass(obj) and issubclass(obj, FactorNode):
    #         class_names.add(obj.__clas__.__name__)
    # return class_names
    klasses = set()
    for name in dir(module):
        obj = getattr(module,name)
        if inspect.isclass(obj) and issubclass(obj, base_class) and obj != base_class:
            klasses.add(obj)
    return klasses

def subclasses_in_package(base_class, package_name):
    '''
    List all subclasses of the base factor class in the package.
    :param package_name:
    :param base_class:
    :return:
    '''
    klasses = set()
    modules, package_path = package_contents(package_name)
    # TODO: This feels hacky... is there a better way?
    _initial_path = sys.path
    sys.path.append(package_path)
    for module_name in modules:
        module = import_module(module_name)
        klasses.update(subclasses_in_module(base_class, module))
    sys.path = _initial_path
    return klasses