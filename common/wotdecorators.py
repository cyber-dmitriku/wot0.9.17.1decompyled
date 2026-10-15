# Source Generated with Decompyle++
# File: wotdecorators.pyc (Python 2.6)

from debug_utils import LOG_WRAPPED_CURRENT_EXCEPTION

def noexcept(func):
    
    def wrapper(*args, **kwArgs):
        
        try:
            return func(*args, **args)
        except:
            LOG_WRAPPED_CURRENT_EXCEPTION(wrapper.__name__, func.__name__, func.func_code.co_filename, func.func_code.co_firstlineno + 1)


    return wrapper


def nofail(func):
    
    def wrapper(*args, **kwArgs):
        
        try:
            return func(*args, **args)
        except:
            LOG_WRAPPED_CURRENT_EXCEPTION(wrapper.__name__, func.__name__, func.func_code.co_filename, func.func_code.co_firstlineno + 1)
            import sys as sys
            sys.exit()


    return wrapper


