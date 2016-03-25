from distutils.core import setup
from distutils.extension import Extension

setup(
    ext_modules=[
        Extension("hello", ["RetrieveInfoHandle.cpp"],
        libraries = ["boost_python"])
    ])