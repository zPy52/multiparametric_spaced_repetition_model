from csv import DictReader
from datetime import datetime
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt

Instance = namedtuple('Instance', ('recall', 'datetime', 'history_seen', 'history_correct'))

def format_history(n: int) -> int:
    if n <= 100:
        return 100
    elif n <= 200:
        return 200
    elif n <= 300:
        return 300
    elif n <= 400:
        return 400
    elif n <= 500:
        return 500
    elif n <= 600:
        return 600
    elif n <= 700:
        return 700
    elif n <= 800:
        return 800
    elif n <= 900:
        return 900
    else:
        return 1000

def build_db():
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
                    int(row['history_correct']), 
                )
            )

    users = tuple(data.keys())
    
    def get_lexemes_of_user(user: str) -> tuple:
        return tuple(data[user].keys())
    
    for user in users:
        lexemes = get_lexemes_of_user(user)
        
        for lexeme in lexemes:
            if len(data[user][lexeme]) >= 20:
                continue
            
            del data[user][lexeme]

    for user in users:
        if len(data[user]) == 0:
            del data[user]

    print('Moving on.')

    return data


data = build_db()


corrects = {}
incorrects = {}

for user in data:
    for lexeme in data[user]:
        right_responses = data[user][lexeme][-1].history_correct
        wrong_responses = data[user][lexeme][-1].history_seen - right_responses
        
        category = format_history(data[user][lexeme][-1].history_seen)
        
        corrects.setdefault(category, [])
        incorrects.setdefault(category, [])
        
        corrects[category].append(right_responses)
        incorrects[category].append(wrong_responses)


totals = {}
for k in corrects:
    corrects[k] = sum(corrects[k]) / len(corrects[k])
    incorrects[k] = sum(incorrects[k]) / len(incorrects[k])

    totals[k] = corrects[k] + incorrects[k]


N = len(corrects)

ind = np.arange(N)
width = 0.35 
 
fig, ax = plt.subplots()
fig.set_size_inches(9.5, 5.0)

corrects = [x[0][1] / x[1] for x in sorted(zip(corrects.items(), totals.values()), key=lambda x: x[0][0])]
incorrects = [x[0][1] / x[1] for x in sorted(zip(incorrects.items(), totals.values()), key=lambda x: x[0][0])]


p1 = plt.bar(ind, corrects, width, color='royalblue')
p2 = plt.bar(ind, incorrects, width,
             bottom=corrects, color='firebrick')
 
plt.xlabel('Number of repetitions')
plt.ylabel('Responses')
plt.title('Proportion of right/wrong responses')
plt.xticks(ind, ('0-100', '100-200', '200-300', '300-400', '400-500', '500-600', '600-700', '700-800', '800-900', '>900'))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend((p2[0], p1[0]), ('Incorrect', 'Correct'), loc='lower center')
 
plt.savefig('testing/right-wrong_proportion.jpg', format='jpg', dpi=1_000)
 
plt.show()