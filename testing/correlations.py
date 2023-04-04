from csv import DictReader
from collections import namedtuple
from datetime import datetime
from utils.algorithms import MSRM as Algorithm
from utils.flashcards import MSRMFlashcard as Flashcard
from math import sqrt, e, pi
from pyperclip import copy as clipboard_copy 

PHI = (1 + sqrt(5)) / 2 

from warnings import filterwarnings
filterwarnings('ignore')

from pprint import pprint
from pandas import DataFrame

Instance = namedtuple('Instance', ('recall', 'datetime', 'history_seen', 'history_correct'))

data = {}

with open('learning_traces.13m.csv', 'r') as file:
    csv = DictReader(file)
    for row in csv:
        recall = float(row['p_recall'])
        
        user_id = row['user_id']
        lexeme = row['lexeme_id']
        
        data.setdefault(user_id, {})
        data[user_id].setdefault(lexeme, [])
        data[user_id][lexeme].append(
            Instance(
                recall, 
                datetime.utcfromtimestamp(int(row['timestamp'])), 
                int(row['history_seen']), 
                int(row['history_correct'])
            )
        )

users = tuple(data.keys())

for user in users:
    lexemes = tuple(data[user].keys())
    
    for lexeme in lexemes:
        data[user][lexeme].sort(key=lambda x: x.history_seen)
        
        if len(data[user][lexeme]) >= 2 and data[user][lexeme][-1].history_seen >= 10:
            data[user][lexeme] = (data[user][lexeme][-2], data[user][lexeme][-1])
            continue
        
        del data[user][lexeme]

for user in users:
    if len(data[user]) == 0:
        del data[user]

print('Moving on.')

d = {}

exponents = (
    (1.25, 0),
    (1.5, 0),
    (1.75, 0), 
    (PHI, 0), (PHI, 6), (PHI, 6 * 2),
    (2, 0), (2, 4), (2, 4 * 2),
    (e, 0), (e, 3), (e, 3 * 2),
    (pi, 0), (pi, 2), (pi, 2 * 2)
)


print('---')
for BASE_EXPONENT in [exponent for exponent in exponents if exponent[1] == 0]:
    d.setdefault(round(BASE_EXPONENT[0], 3), {})
    
    measure_max = (BASE_EXPONENT[0] ** BASE_EXPONENT[1])
    #graduating_prowess_factor = 180 / (BASE_EXPONENT[1] - log(0.95 * measure_max, BASE_EXPONENT[0]))
    def get_expected_response(days, prowess_factor) -> float:
        """if prowess_factor >= graduating_prowess_factor:
            return 1.0"""
        
        return (BASE_EXPONENT[0] ** (-(days - BASE_EXPONENT[1] * prowess_factor) / prowess_factor)) / measure_max


    def corr_core(a, b, c):
        corr = {'prediction': [], 'actual': []}

        for user in data:
            for lexeme in data[user]:
                card = Flashcard(lexeme, '', data[user][lexeme][0].datetime)
                algorithm = Algorithm([card], a, b, c)
                
                for _ in range(data[user][lexeme][1].history_seen - data[user][lexeme][1].history_correct):
                    algorithm.evaluate(-1)
                
                for _ in range(data[user][lexeme][1].history_correct):
                    algorithm.evaluate(1)
                
                
                difference_in_days = (data[user][lexeme][1].datetime - data[user][lexeme][0].datetime).total_seconds() / 60 / 60 / 24
                
                expected_response = get_expected_response(difference_in_days, card.prowess_factor)
                
                
                corr['prediction'].append(expected_response)
                corr['actual'].append(data[user][lexeme][1].recall)
        
        df = DataFrame(corr)
        
        return {'pearson': df.corr(method='pearson').to_dict('records')[0]['actual'], 
                'spearman': df.corr(method='spearman').to_dict('records')[0]['actual'], 
                'kendall': df.corr(method='kendall').to_dict('records')[0]['actual']}
                    
        

    result = corr_core(2.0, 2.0, 2.0)

    d[round(BASE_EXPONENT[0], 3)][BASE_EXPONENT[1]] = result
    print(BASE_EXPONENT[0], '-', BASE_EXPONENT[1])
    pprint(result)
    print('---')

print('DATA DICT COPIED TO THE CLIPBOARD')

clipboard_copy(str(d))