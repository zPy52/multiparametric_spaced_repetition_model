#cython: language_level=3

from datetime import datetime

cdef class MSRMFlashcard:
	def __init__(self, str public, str private, object next_date, bint exam_phase = False):
		if not isinstance(next_date, datetime):
			raise TypeError('Invalid datetime object.')

		self.public = public
		self.private = private
		self.next_date = next_date
		self.exam_phase = exam_phase

		self.__ease_factor = 1.0
		self.__prowess_factor = 0.0425

	@property
	def ease_factor(self):
		return self.__ease_factor
    
	@ease_factor.setter
	def ease_factor(self, double value):
		self.__ease_factor = value if value > 0.1 else 0.1


	@property
	def prowess_factor(self):
		return self.__prowess_factor
    
	@prowess_factor.setter
	def prowess_factor(self, double value):
		# "Restart" the Flashcard progress/data when the user gets struck.
		if value < 0.0125:
			self.__prowess_factor = 0.0125
		else:
			self.__prowess_factor = value


cdef class LeitnerFlashcard:
	def __init__(self, str public, str private, object next_date, double box = 1.0):
		self.public = public
		self.private = private
		self.next_date = next_date
		self.box = box


cdef class PimsleurFlashcard:
	def __init__(self, str public, str private, object next_date, int stage = 1):
		self.public = public
		self.private = private
		self.next_date = next_date
		self.__stage = stage

	@property
	def stage(self):
		return self.__stage

	@stage.setter
	def stage(self, int value):
		if value >= 1 and value <= 11:
			self.__stage = value
