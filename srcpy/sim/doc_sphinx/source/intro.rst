Introduction
============
The project was started to prepare complete set of functions to both simulate and implement procedures and blocks of a Navigation Software Defined Radio (NavSDR).

First set of functions is prepared to generate digitalized version of radio signals in both baseband and passband. Resuting signals are stored in form of NumPy arrays. These functions form a transmitter functionality of the NavSDR.

Secondly the correlators were prepared to measure time-delay between two signals or a signals and its own copy. These functions are based on the parallel processing using two different libraries -- MKL library by Intel and Cuda library by NVidia.

Dependencies:
-------------
Python 3.6, Numpy 1.12.1, Accelerate 2.3.1, Accelerate Cudalib 2.0;
Note: All packages were installed as part of the Anaconda  4.3.24 and Python 3.6.2 running on the platform linux-64

Installation
------------
No special operation required. All what needs to be done is to save entire ''srcpy'' folder with its contents and use any function. Once they are called from the ''srcpy'' folder they should work immediatelly, otherwise make sure you have the ''srcpy'' folder included in your python system path.
