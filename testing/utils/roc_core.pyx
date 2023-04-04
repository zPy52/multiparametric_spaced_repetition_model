#cython: language_level=3
from threading import Lock

from utils.build_db import build_db
from utils.db_utils cimport format_response, classify_expected_response
from utils.flashcard cimport Flashcard
from utils.algorithm cimport Algorithm

cdef class ROC:
	cdef public int TP, FP, TN, FN
	def __init__(self, int TP, int FP, int TN, int FN):
		self.TP = TP
		self.FP = FP
		self.TN = TN
		self.FN = FN

cdef dict data = build_db('learning_traces.13m.csv')
cdef dict result = {}
lock = Lock()

cdef ROC roc_core(double a, double b, double c, double threshold):
	global data

	cdef int TP, FP, TN, FN, n
	cdef str user, lexeme
	cdef double difference_in_days, expected_response
	cdef Flashcard card
	cdef Algorithm algorithm

	TP, FP, TN, FN = 0, 0, 0, 0

	for user in data:
		for lexeme in data[user]:
			for n in range(1, len(data[user][lexeme])):
				card = Flashcard(lexeme, '', data[user][lexeme][n - 1].date)
				algorithm = Algorithm(card, a, b, c)
                
				for _ in range(data[user][lexeme][n].history_seen - data[user][lexeme][n].history_correct):
					algorithm.evaluate(-1)
                
				for _ in range(data[user][lexeme][n].history_correct):
					algorithm.evaluate(1)
                
				difference_in_days = (data[user][lexeme][n].date - data[user][lexeme][n - 1].date).total_seconds() / 60 / 60 / 24
                
				expected_response = classify_expected_response(difference_in_days, card.prowess_factor, threshold)
                
				if expected_response == 1:
					if expected_response == format_response(data[user][lexeme][n].recall):
						TP += 1
					else:
						FP += 1
				else:
					if expected_response == format_response(data[user][lexeme][n].recall):
						TN += 1
					else:
						FN += 1
	
	return ROC(TP, FP, TN, FN)

cdef double calculate_exact_bar_area(double[2] coord1, double[2] coord2):
	if abs(coord1[1] - coord2[1]) < 10 ** (-15):
		return abs(coord1[0] - coord2[0]) * coord1[1]
        
	M = coord1 if coord1[1] >= coord2[1] else coord2
	m = coord1 if coord1[1] < coord2[1] else coord2

	x = abs(M[0] - m[0])
	y = abs(M[1] - m[1])
        
	return x * M[1] - (x * y) / 2.0

cdef double calculate_area(tuple x, tuple y):
	cdef double T, UT, US, auc, x_coord, y_coord
	cdef double[2] last_bar, new_bar

	T = (x[0] * y[0]) / 2.0
	UT = ((1.0 - x[-1]) * (1.0 - y[-1])) / 2.0
	US = (1.0 - x[-1]) * y[-1]

	auc = T + UT + US

	last_bar = [x[1], y[1]]
	for x_coord, y_coord in zip(x[2:-1], y[2:-1]):
		new_bar = [x_coord, y_coord]
		auc += calculate_exact_bar_area(last_bar, new_bar)
		last_bar = new_bar
        
	return auc


cpdef main(double a, double b, double c, double threshold):
	global result
	global lock

	cdef ROC roc
	cdef double sensivity, one_minus_specificity
    
	roc = roc_core(a, b, c, threshold)

	sensivity = roc.TP / (roc.TP + roc.FN)
	one_minus_specificity = 1.0 - roc.TN / (roc.TN + roc.FP)

	print(f'Threshold of {threshold} ({a}-{b}-{c}):', (one_minus_specificity, sensivity))

	with lock:
		result.setdefault(str(a), {})
		result[str(a)].setdefault(str(b), [])
		result[str(a)][str(b)].append((one_minus_specificity, sensivity))

cdef format_result():
	global result

	for ac in result:
		for b in result[ac]:
			result[ac][b].sort()
			result[ac][b] = calculate_area(
				tuple([xy[0] for xy in result[ac][b]]), 
				tuple([xy[1] for xy in result[ac][b]])
			)

cpdef dict get_result():
	format_result()
	global result

	return result