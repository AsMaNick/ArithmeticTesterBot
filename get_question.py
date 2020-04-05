def get_question_by_id(id):
    if id == '1':
        a = np.random.randint(1, 200) / 10
        b = np.random.randint(1, 200) / 10
        tp = np.random.randint(5)
        if tp == 0:
            res = '{} - {}'.format(a, b)
        elif tp == 1:
            res = '-{} - {}'.format(a, b)
        elif tp == 2:
            res = '-{} + {}'.format(a, b)
        elif tp == 3:
            res = '-{} + (-{})'.format(a, b)
        elif tp == 4:
            res = '{} + (-{})'.format(a, b)
        return 'Вычисли: '.format(res), eval(res)
    
    
def get_question(test):
    ids = [question.question_id for question in test.questions]
    id = np.random.choice(ids, 1)[0]
    return get_question_by_id(id)