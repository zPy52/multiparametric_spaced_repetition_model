#cython: language_level=3

from libc.math cimport e, sqrt
cdef double PHI = (1.0 + sqrt(5.0)) / 2.0

from utils.nonstaticgaussbell cimport NonStaticGaussBell
from utils.flashcards cimport MSRMFlashcard, LeitnerFlashcard, PimsleurFlashcard

from math import log
from datetime import datetime, timedelta


cdef class MSRM:
	def __init__(self, MSRMFlashcard flashcard, double a = 2.0, double b = 2.0, double c = 2.0):
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


cdef class LeitnerSystem:
	def __init__(self, LeitnerFlashcard flashcard):
		self.flashcard = flashcard

	cdef void evaluate(self, int response):
		if self.flashcard.box > 180:
			return

		if response == 1:
			self.flashcard.box *= 2.0
		else:
			self.flashcard.box /= 2.0

		self.flashcard.next_date += timedelta(days=self.flashcard.box)


cdef class PimsleurSystem:
	def __init__(self, PimsleurFlashcard flashcard):
		self.flashcard = flashcard

	cdef object __stage_to_timedelta(self):
		if self.flashcard.stage == 1:
			return timedelta(seconds=5)
		elif self.flashcard.stage == 2:
			return timedelta(seconds=25)
		elif self.flashcard.stage == 3:
			return timedelta(minutes=2)
		elif self.flashcard.stage == 4:
			return timedelta(minutes=10)
		elif self.flashcard.stage == 5:
			return timedelta(hours=1)
		elif self.flashcard.stage == 6:
			return timedelta(hours=5)
		elif self.flashcard.stage == 7:
			return timedelta(days=1)
		elif self.flashcard.stage == 8:
			return timedelta(days=5)
		elif self.flashcard.stage == 9:
			return timedelta(days=25)
		elif self.flashcard.stage == 10:
			return timedelta(days=4 * 30)
		else:
			return timedelta(days=365 * 2)

	cdef void evaluate(self, int response):
		if self.flashcard.stage == 11:
			return

		self.flashcard.stage += 1

		self.flashcard.next_date += self.__stage_to_timedelta()