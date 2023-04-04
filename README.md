# Multiparametric Spaced Repetition Model

Copyright (c) 2023 Antonio Peña Peña. MIT License.

This repository contains the code employed for testing purposes of the paper _An Optimized Multiparametric Spaced Repetition Model for Improved Memorability_.

## Language & Packages
We employ Python and Cython to devise the logic of every program written. Some external packages are also utilised. These are the versions installed:

- `Python`: 3.11.1
- `Cython`: 0.29.33
- `matplotlib`: 3.6.2
- `numpy`: 1.24.0
- `pandas`: 1.5.2

In order to effectively install Cython, it's not enough to run `pip3 install Cython`, but you also need a C Compiler such as GCC or Microsoft Visual C/C++ installed in your computer. For detailed guidelines on installation, you can visit the official [web page](https://cython.readthedocs.io/en/latest/src/quickstart/install.html).

## Dataset
The dataset used for this research is the one provided by [Settles and Meeder](https://github.com/duolingo/halflife-regression) (2016) and is available on [Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/N8XJME).

## Compiling code and execution instructions
Cython code must be compiled before running. You can easily do so by going to the pertinent directory (`cd testing`) and going to the Terminal/Command Prompt and running `py compiler.py build_ext --inplace`. That command will automatically _cythonize_ every `.pyx` file in the `testing/utils` subfolder.

Regarding general guidelines to execute the code, it has been designed so that the reader should go to the adecuate directory with the `cd` command and then, right in the desired folder, run the sought code file.