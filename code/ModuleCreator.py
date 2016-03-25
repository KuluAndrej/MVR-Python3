from distutils.core import setup
from distutils.extension import Extension

setup(
    ext_modules=[
        Extension("mutator", ["Mutator.cpp"],
        libraries = ["boost_python"])
    ])