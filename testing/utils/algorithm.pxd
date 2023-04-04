#cython: language_level=3

from utils.nonstaticgaussbell cimport NonStaticGaussBell
from utils.flashcard cimport Flashcard

cdef double PHI

cdef class Algorithm:
	cdef public Flashcard flashcard
	cdef NonStaticGaussBell __gauss

	cdef double __get_interval_in_days(self, double prowess_factor)
	cdef void evaluate(self, int response)