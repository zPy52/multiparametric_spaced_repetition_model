#cython: language_level=3

from libc.math cimport sqrt
from math import log

cdef int format_response(double p_recall):
    if p_recall >= 0.5:
        return 1
    else:
        return -1


cdef double[2] BASE_EXPONENT = [(1.0 + sqrt(5.0)) / 2.0, 6.0]
cdef double measure_max = BASE_EXPONENT[0] ** BASE_EXPONENT[1]

cdef double graduating_prowess_factor = 180.0 / (BASE_EXPONENT[1] - log(0.95 * measure_max, BASE_EXPONENT[0]))

cdef double get_expected_response(double days, double prowess_factor):
    if prowess_factor >= graduating_prowess_factor:
        return 1.0
        
    return (BASE_EXPONENT[0] ** (-(days - BASE_EXPONENT[1] * prowess_factor) / prowess_factor)) / measure_max


cdef int classify_expected_response(double days, double prowess_factor, double threshold):
    cdef double prediction
    prediction = (BASE_EXPONENT[0] ** (-(days - BASE_EXPONENT[1] * prowess_factor) / prowess_factor)) / measure_max
    
    if prediction >= threshold:
        return 1
    else:
        return -1