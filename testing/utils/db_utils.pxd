#cython: language_level=3

cdef int format_response(double p_recall)

cdef double[2] BASE_EXPONENT
cdef double measure_max
cdef double graduating_prowess_factor

cdef double get_expected_response(double days, double prowess_factor)

cdef int classify_expected_response(double days, double prowess_factor, double threshold)