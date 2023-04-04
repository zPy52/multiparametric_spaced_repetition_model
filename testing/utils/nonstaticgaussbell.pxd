#cython: language_level=3

cdef class NonStaticGaussBell:
	cdef double a, b, c

	cdef double evaluate(self, int response, double ease_factor)

	cdef double right_response(self, double ease_factor)
	cdef double regular_response(self, double ease_factor)
	cdef double wrong_response(self, double ease_factor)