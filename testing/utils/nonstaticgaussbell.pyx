#cython: language_level=3

from libc.math cimport e

cdef class NonStaticGaussBell:
    def __init__(self, double a, double b, double c):
        self.a, self.b, self.c = a, b, c

    cdef double evaluate(self, int response, double ease_factor):
        if response == 1:
            return self.right_response(ease_factor)
        elif response == 0:
            return self.regular_response(ease_factor)
        elif response == -1:
            return self.wrong_response(ease_factor)
        
        raise ValueError('Invalid response value.')

    cdef double right_response(self, double ease_factor):
        return ease_factor * self.a * (e ** (-(self.b ** 2.0) / (2.0 * (self.c ** 2.0)))) + 2.0
        
    cdef double regular_response(self, double ease_factor):
        return self.right_response(ease_factor) / 2.0

    cdef double wrong_response(self, double ease_factor):
        cdef double result
        result = ease_factor * (self.a / 4.0) + 0.25
        return result if result <= 0.8 else 0.8