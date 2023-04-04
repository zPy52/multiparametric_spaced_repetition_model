#cython: language_level=3

from libc.math cimport sqrt
cdef double PHI = (1.0 + sqrt(5.0)) / 2.0

from utils.nonstaticgaussbell cimport NonStaticGaussBell
from utils.flashcard cimport Flashcard

from math import log
from datetime import datetime, timedelta


cdef class Algorithm:
	def __init__(self, Flashcard flashcard, double a = 2.0, double b = 2.0, double c = 2.0):
		self.flashcard = flashcard
        
		self.__gauss = NonStaticGaussBell(a, b, c)

	cdef double __get_interval_in_days(self, double prowess_factor):
		# If 16 is 100%, 17.0471 is 84.13%. It's supposed that the user would remember 84.13% of the content.
		return prowess_factor * (6.0 - log(17.0471, PHI))

	cdef void evaluate(self, int response):
		'''Evaluate the first card of the list available.'''

		# The response can be -1, 0 or 1, for bad, regular and good, respectively.
		if self.flashcard.exam_phase:
			self.flashcard.exam_phase = False
			if response == -1:
				self.flashcard.ease_factor *= 0.5
			elif response == 0:
				self.flashcard.ease_factor *= 0.65
			elif response == -1:
				self.flashcard.ease_factor *= 0.8

		else:
			if response == -1:
				self.flashcard.exam_phase = True
			else:
				if response == 0:
					self.flashcard.ease_factor *= 0.9
				elif response == 1:
					self.flashcard.ease_factor *= 1.2

		self.flashcard.prowess_factor *= self.__gauss.evaluate(response, self.flashcard.ease_factor)

		if self.flashcard.exam_phase:
			if self.flashcard.prowess_factor < 0.0425:
				self.flashcard.next_date += timedelta(days=self.__get_interval_in_days(0.0425))
			
			else:
				self.flashcard.next_date += timedelta(days=min(
						self.__get_interval_in_days(self.flashcard.prowess_factor),
						1.0)
				)

		else:
			days = self.__get_interval_in_days(self.flashcard.prowess_factor)
			
			if 2030 > self.flashcard.next_date.year + days / 365:
				self.flashcard.next_date = self.flashcard.next_date + timedelta(days=days)
			
			else:
				self.flashcard.next_date = datetime(7500, 1, 1)