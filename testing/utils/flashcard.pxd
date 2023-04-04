#cython: language_level=3

cdef class Flashcard:
	cdef public str public, private
	cdef public object next_date
	cdef public bint exam_phase

	cdef double __ease_factor, __prowess_factor