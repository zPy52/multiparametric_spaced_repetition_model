#cython: language_level=3

cdef class MSRMFlashcard:
	cdef public str public, private
	cdef public object next_date
	cdef public bint exam_phase

	cdef double __ease_factor, __prowess_factor

cdef class SuperMemo2Flashcard:
	cdef public int repetitions, interval
	cdef public double easiness
	cdef object __next_date

cdef class LeitnerFlashcard:
	cdef public str public, private
	cdef public object next_date
	cdef public double box

cdef class PimsleurFlashcard:
	cdef public str public, private
	cdef public object next_date
	cdef int __stage