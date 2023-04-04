##### IMPORTANT: FOR IT TO WORK RUN THE FOLLOWING IN THE COMMAND PROMPT:
# py compiler.py build_ext --inplace

from os import walk
from pathlib import Path

from setuptools import setup
from Cython.Build import cythonize


# Compile every Cython file.
for foldername, _, filenames in walk('utils'):
    for filename in filenames:
        if filename[-3:].lower() != 'pyx':
            continue
        
        setup(
            name=filename[:-4],
            ext_modules=cythonize(f'{foldername}/{filename}'),
            zip_safe=False,
        )

# Remove redundant & unnecesary .c files.
for foldername, _, filenames in walk('utils'):
    for filename in filenames:
        if filename.lower().endswith('.c'):
            Path(foldername + '/' + filename).unlink()