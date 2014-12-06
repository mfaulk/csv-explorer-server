def get_instance(class_name, context, extensions_path='framework.extensions', args=None):
    '''
    Obtain an instance of a Factor Graph node by class name.
    :param class_name:
    :param extensions_path:
    :return: Instance of class, or None
    '''
    if args is None: args = dict()
    instance = None
    module  = _import_module_in_package('factors.nodes')
    if hasattr(module, class_name):
        class_ = getattr(module, class_name)
        instance = class_(context, args)
    else:
        instance = get_instance_from_extensions(class_name, context, extensions_path, args=args)
    return instance

def get_instance_from_extensions(class_name, context, extensions_path, args=None):
    if args is None: args = dict()
    module_name = camel_case_to_lower_case_underscore(class_name)
    module_path = extensions_path + '.' + module_name
    module = _import_module_in_package(module_path)
    class_ = getattr(module, class_name)
    return class_(context, args)

def _import_module_in_package(name):
    '''
    Helper function to drill down to the requested package: __import__ returns the top-level package.
    :param name: module name
    :return: module
    '''
    m = __import__(name)
    for n in name.split(".")[1:]:
       m = getattr(m, n)
    return m
    #m = importlib.import_module(name)
    #return m


def camel_case_to_lower_case_underscore(string):
    """
    Split string by upper case letters.

    F.e. useful to convert camel case strings to underscore separated ones.

    @return words (list)
    """
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(string):
        if char.isupper() and from_char_position < current_char_position:
            words.append(string[from_char_position:current_char_position].lower())
            from_char_position = current_char_position
    words.append(string[from_char_position:].lower())
    return '_'.join(words)