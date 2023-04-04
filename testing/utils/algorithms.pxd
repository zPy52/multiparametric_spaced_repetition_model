#cython: language_level=3

from utils.nonstaticgaussbell cimport NonStaticGaussBell
from utils.flashcards cimport MSRMFlashcard, LeitnerFlashcard, PimsleurFlashcard

cdef double PHI

cdef class MSRM:
	cdef public MSRMFlashcard flashcard
	cdef NonStaticGaussBell __gauss

	cdef double __get_interval_in_days(self, double prowess_factor)
	cdef void evaluate(self, int response)


cdef class LeitnerSystem:
	cdef public LeitnerFlashcard flashcard

	cdef void evaluate(self, int response)


cdef class PimsleurSystem:
	cdef public PimsleurFlashcard flashcard

	cdef object __stage_to_timedelta(self)

	cdef void evaluate(self, int response)