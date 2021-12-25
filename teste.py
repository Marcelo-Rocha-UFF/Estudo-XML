import ctypes
import sys

def get_python_interpreter_arguments():
    argc = ctypes.c_int()
    argv = ctypes.POINTER(ctypes.c_wchar_p if sys.version_info >= (3, ) else ctypes.c_char_p)()
    ctypes.pythonapi.Py_GetArgcArgv(ctypes.byref(argc), ctypes.byref(argv))
    arguments = list()
    for i in range(argc.value - len(sys.argv) + 1):
        arguments.append(argv[i])
    return arguments

get_python_interpreter_arguments()

print(get_python_interpreter_arguments()[0])