import numpy as np
from utils import get_str_value, round_to


def get_question_by_id(id):
    if id <= 2:
        a = np.random.randint(1, 51)
        b = np.random.randint(1, 51)
        if id == 2:
            a = get_str_value(np.random.randint(1, 100) / 10)
            b = get_str_value(np.random.randint(1, 100) / 10)
        all = ['{} - {}'.format(a, b),
               '-{} - {}'.format(a, b),
               '-{} + {}'.format(a, b),
               '-{} + (-{})'.format(a, b),
               '{} + (-{})'.format(a, b),
               '-{} - (-{})'.format(a, b),
               '{} - (-{})'.format(a, b),
               '-{} - (-{})'.format(a, b),
               '-(-{}) + {}'.format(a, b),
               '-(-{}) - {}'.format(a, b)]
        res = np.random.choice(all, 1)[0]
        return 'Вычисли: {}'.format(res), eval(res)
    
    
def get_question(test):
    ids = [question.question_id for question in test.questions]
    id = np.random.choice(ids, 1)[0]
    return get_question_by_id(id)