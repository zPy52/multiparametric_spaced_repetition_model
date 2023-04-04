#cython: language_level=3
from threading import Lock
from utils.build_db import build_db
from utils.db_utils cimport get_expected_response
from utils.flashcard cimport Flashcard
from utils.algorithm cimport Algorithm

cdef dict data = build_db('learning_traces.13m.csv')

lock = Lock()

cdef dict xy = {}

cpdef tuple main(double a, double b, double c):
    global data
    global xy
    global lock

    cdef str user, lexeme
    cdef int n
    cdef double difference_in_days, expected_response
    cdef list maes = []

    cdef Flashcard card
    cdef Algorithm algorithm

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
                    
                expected_response = get_expected_response(difference_in_days, card.prowess_factor)
                
                maes.append(abs(data[user][lexeme][n].recall - expected_response))
            
    with lock:
        xy.setdefault(str(a), {})
        xy[str(a)][str(b)] = sum(maes) / len(maes)

def get_result():
    global xy
    return xy