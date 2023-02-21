from __future__ import annotations
from math import e, log2
from random import choices

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from typing import List, Tuple, Set


class AlgorithmGaussBell: # Suited for the algorithm.
    __slots__ = '__a', '__b', '__c'

    def __init__(self) -> AlgorithmGaussBell:
        self.__a, self.__b, self.__c = 2.0, 3.0, 2.0
    
    def __call__(self, response: int, trials: int) -> float:
        if not isinstance(response, int) or not isinstance(trials, int):
            raise ValueError('Invalid inputs: at least one of them is not an integer.')
        
        trials /= 10

        functions = {1: self.__right_response, 0: self.__regular_response, -1: self.__wrong_response}

        result = functions[response](trials)

        return result if trials <= self.__b else self.__max_values(response)

    def __right_response(self, x: int | float) -> float:
        return self.__a * (e ** (-((x - self.__b) ** 2) / (2 * (self.__c ** 2)))) + 2
        
    def __regular_response(self, x: int | float) -> float:
        return e ** (-((x - self.__b) ** 2) / (2 * (self.__c ** 2))) + 1.05

    def __wrong_response(self, x: int | float) -> float:
        return 0.5 * (e ** (-(x ** 2) / 2)) + 0.35
    
    def __max_values(self, response: int) -> float:
        if response == 1:
            return self.__right_response(self.__b)
        if response == 0:
            return self.__regular_response(self.__b)
        if response == -1:
            return self.__wrong_response(self.__b)
        else:
            raise ValueError('Invalid integer input. Only 1 (right), 0 (regular), and -1 (wrong) are accepted.')
        

print(AlgorithmGaussBell()(1, 1), AlgorithmGaussBell()(1, 3), AlgorithmGaussBell()(1, 10))
print(AlgorithmGaussBell()(0, 1), AlgorithmGaussBell()(0, 3), AlgorithmGaussBell()(0, 10))
print(AlgorithmGaussBell()(-1, 1), AlgorithmGaussBell()(-1, 3), AlgorithmGaussBell()(-1, 10))


class FlashcardTrials:
    __slots__ = '__rights', '__regulars', '__wrongs'

    def __init__(self) -> FlashcardTrials:
        self.__rights, self.__regulars, self.__wrongs = 0, 0, 0
    
    def did_attempt(self, response: int) -> None:
        if response not in {-1, 0, 1}:
            raise ValueError('Invalid response value.')

        if response == -1:
            self.__wrongs += 1
        if response == 0:
            self.__regulars += 1
        if response == 1:
            self.__rights += 1
    
    @property
    def right_attempts(self) -> int:
        return self.__rights
    
    @property
    def regular_attempts(self) -> int:
        return self.__regulars

    @property
    def wrong_attempts(self) -> int:
        return self.__wrongs

@dataclass
class Flashcard:
    # Content of the flashcard. E.g., problem statement and its solution.
    public: str
    private: str

    # Next reviewing date.
    next_date: datetime

    # Store if the user failed in the last review.
    exam_phase: bool = field(default=False)

    def __post_init__(self) -> Flashcard:
        self.__trials: FlashcardTrials = FlashcardTrials()
        
        # Algorithm needed parameters.
        self.__ease_factor: float = 1.0
        self.__increment_rate: List[float] = [1.0]
        self.__prowess_factor: float = 0.0125


    @property
    def trials(self) -> int:
        return self.__trials
    
    @trials.setter
    def trials(self, _: object) -> None:
        raise TypeError("Cannot modify directly the number of trials. Did you mean using 'make_attempt()'?")


    @property
    def ease_factor(self) -> float:
        return self.__ease_factor
    
    @ease_factor.setter
    def ease_factor(self, value: int | float) -> None:
        if isinstance(value, int):
            value = float(value)
        
        if not isinstance(value, float):
            raise ValueError('Cannot assign a non-int or -float value to the ease factor.')
        
        self.__ease_factor = value


    @property
    def prowess_factor(self) -> float:
        return self.__prowess_factor
    
    @prowess_factor.setter
    def prowess_factor(self, value: int | float) -> None:
        if isinstance(value, int):
            value = float(value)

        if not isinstance(value, float):
            raise ValueError('Cannot assign a non-int or -float value.')
        
        # Restart the Flashcard progress/data when the user gets struck.
        if value <= 0.0125:
            self.__increment_rate = [1.0]
            self.__prowess_factor = 0.0125
        else:
            self.__prowess_factor = value


    def push_increment_rate(self, increment: int | float) -> None:
        self.__increment_rate.append(self.__increment_rate[-1] * increment)

    def total_increment_rate(self) -> float:
        return sum(self.__increment_rate)
    
    def total_mul_inc_rate(self) -> float:
        result = 0.0125
        for i in self.__increment_rate:
            result *= i * self.__ease_factor
        return result

    def did_attempt(self, response: int) -> FlashcardTrials:
        self.__trials.did_attempt(response)
        return self.__trials


class Algorithm(list):
    def __init__(self, flashcards: List[Flashcard] | Tuple[Flashcard] | Set[Flashcard]) -> Algorithm[Flashcard]:
        if not isinstance(flashcards, (list, tuple, set)):
            raise ValueError('Unable to handle a non-list, -tuple or -set object.') 
        
        for element in flashcards:
            if not isinstance(element, Flashcard):
                raise ValueError('The algorithm only supports Flashcard objects as its components.')
        
        super().__init__(flashcards)

        self.__gauss_bell = AlgorithmGaussBell()

    def __str__(self) -> str:
        return 'Algorithm([' + ', '.join([str(flashcard) for flashcard in self]) + '])'

    def __get_interval_in_days(self, prowess_factor: int | float) -> float:
        # If 16 is 100%, 11.2 is 70%. It's supposed that the user would remember 70% of the content.
        review_when_only_remember = 0.7
        return prowess_factor * (4.0 - log2(review_when_only_remember * 16.0))

    def append(self, element: Flashcard) -> None:
        if not isinstance(element, Flashcard):
            raise ValueError('The algorithm only supports Flashcard objects.')
        
        super().append(element)

    def pop(self, index: int) -> Flashcard:
        return super().pop(index)

    def sort(self) -> None:
        super().sort(key=lambda flashcard: flashcard.next_date)

    def evaluate(self, response: int) -> None:
        '''Evaluate the first card of the list available.'''

        card: Flashcard = self[0]

        trials = card.did_attempt(response)
        trials = {-1: trials.wrong_attempts, 0: trials.regular_attempts, 1: trials.right_attempts}

        # The response can be -1, 0 or 1, for bad, regular and good, respectively.
        if card.exam_phase:
            card.exam_phase = False

            if response == 1:
                card.ease_factor *= 0.9
            if response == 0:
                card.ease_factor *= 0.75
            if response == -1:
                card.ease_factor *= 0.65


            card.push_increment_rate(self.__gauss_bell(response, trials[response]))
            card.prowess_factor = card.total_mul_inc_rate()
        else:
            card.push_increment_rate(self.__gauss_bell(response, trials[response]))

            if response == -1:
                card.prowess_factor = 0.0125
                card.exam_phase = True
            else:
                if response == 0:
                    card.ease_factor *= 0.95
                if response == 1:
                    card.ease_factor *= 1.1

                card.prowess_factor = card.total_mul_inc_rate()
        
        # TODO: If card's prowess_factor >= 810, remove from List and store it on disk.

        try:
            #card.next_date = datetime.utcnow() + timedelta(days=self.__get_interval_in_days(card.prowess_factor))
            card.next_date = card.next_date + timedelta(days=self.__get_interval_in_days(card.prowess_factor))
        except OverflowError:
            card.next_date = datetime(9999, 1, 1)

        self[0] = card

        self.sort()

@dataclass
class AnkiFlashcard:
    public: str
    private: str

    exam_phase: bool = field(default=False)

    ease: float = field(default=2.5)
    interval_modifier: float = field(default=1.0)
    interval: float = field(default=0.0104167)# Let's say interval in days (15 min).

    def __post_init__(self):
        self.__trials: int = 0

    def make_attempt(self):
        self.__trials += 1
        return self.__trials
    
    @property
    def trials(self):
        return self.__trials



class AnkiAlgorithm(list):
    def __init__(self, flashcards: List[AnkiFlashcard] | Tuple[AnkiFlashcard] | Set[AnkiFlashcard]) -> AnkiAlgorithm[AnkiFlashcard]:
        if not isinstance(flashcards, (list, tuple, set)):
            raise ValueError('Unable to handle a non-list, -tuple or -set object.') 
        
        for element in flashcards:
            if not isinstance(element, AnkiFlashcard):
                raise ValueError('The algorithm only supports Flashcard objects as its components.')
        
        super().__init__(flashcards)

    def __str__(self) -> str:
        return 'AnkiAlgorithm([' + ', '.join([str(flashcard) for flashcard in self]) + '])'

    def append(self, element: AnkiFlashcard) -> None:
        if not isinstance(element, AnkiFlashcard):
            raise ValueError('The algorithm only supports AnkiFlashcard objects.')
        
        super().append(element)

    def pop(self, index: int) -> AnkiFlashcard:
        return super().pop(index)

    def sort(self) -> None:
        super().sort(key=lambda flashcard: flashcard.interval)

    def evaluate(self, response: int) -> None:
        '''Evaluate the first card of the list available.'''

        card: AnkiFlashcard = self[0]

        # The response can be -1, 0 or 1, for bad, regular and good, respectively.
        if card.exam_phase:
            card.exam_phase = False

            if response == 1:
                card.interval *= 1
            if response == 0:
                card.interval *= 0.9
            if response == -1:
                card.ease *= 0.8
                card.interval *= 0.5
                card.exam_phase = True

        else:
            if response == -1:
                card.ease *= 0.8
                card.interval *= 0.5
                card.exam_phase = True
            else:
                if response == 0:
                    card.ease *= 0.85
                    card.interval = card.interval * 1.2 * card.interval_modifier
                if response == 1:
                    card.interval = card.interval * card.ease * card.interval_modifier

        card.interval = card.interval if card.interval >= 0.0104167 else 0.0104167

        self[0] = card

        self.sort()





class Automaton:
    def __init__(self):
        self.__trials = 0
        self.attempts = []

        self.genius_grade = 0.05
    
    def make_attempt(self):
        probabilities = [0.0, 0.0, 0.0]

        for _ in range(self.__trials):
            if probabilities[0] < 0.7:
                probabilities[0] += self.genius_grade
            else:
                break
        
        rest = 1 - probabilities[0]

        probabilities[1] = rest * 0.7
        probabilities[2] = rest - probabilities[1]

        response = choices([1, 0, -1], weights=probabilities)[0]

        self.attempts.append(response)

        self.__trials += 1

        return response


if __name__ == '__main__':
    print('--- NEW TEST ---')

    automatons = [Automaton() for _ in range(3)]
    for i in range(30):
        for automaton in automatons:
            automaton.make_attempt()

    my_means = []

    for i, automaton in enumerate(automatons):
        algorithm = Algorithm([Flashcard('public content', 'private content', datetime.utcnow())])

        #print('###')
        #print(f'Automaton {i + 1}:', automaton.attempts)

        dates = []
        counter = 0
        for attempt in [-1, 0, -1, 1, 1, -1, 0, 0, 1, 1] + [1] * 10:
            if algorithm[0].prowess_factor >= 810:
                break
            
            counter += 1
            
            algorithm.evaluate(attempt)

            dates.append(str(algorithm[0].next_date))
        
        print('###')
        print(automaton.attempts)
        print(dates)

        my_means.append(counter)

        #print(f'Next date: {algorithm[0].next_date}', f'Prowess factor: {algorithm[0].prowess_factor}', sep='\n')
    print(sum(my_means) / len(my_means))


