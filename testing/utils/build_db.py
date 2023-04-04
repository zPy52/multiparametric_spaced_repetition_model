from dataclasses import dataclass
from datetime import datetime
from csv import DictReader

@dataclass
class Instance:
    recall: float
    date: datetime
    history_seen: int
    history_correct: int


def build_db(filepath: str) -> dict:
    data = {}
    with open(filepath, 'r') as file:
        csv = DictReader(file)

        for row in csv:
            recall = float(row['p_recall'])
            
            user = row['user_id']
            lexeme = row['lexeme_id']
            
            data.setdefault(user, {})
            data[user].setdefault(lexeme, [])
            data[user][lexeme].append(
                Instance(
                    recall, 
                    datetime.utcfromtimestamp(int(row['timestamp'])), 
                    int(row['history_seen']), 
                    int(row['history_correct']), 
                )
            )
    
    for user in tuple(data.keys()):
        lexemes = tuple(data[user].keys())
        
        for lexeme in lexemes:
            if len(data[user][lexeme]) >= 2:
                data[user][lexeme].sort(key=lambda x: x.history_seen)
                data[user][lexeme] = [instance for instance in data[user][lexeme] if instance.history_seen >= 10]

                if len(data[user][lexeme]) == 0:
                    del data[user][lexeme]

                continue
            
            del data[user][lexeme]

        if len(data[user]) == 0:
            del data[user]

    print('Moving on.')

    return data