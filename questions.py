import numpy as np
from utils import get_str_value, get_signed_value, round_to, is_equal


def get_square_equation(a, p=None):
    if p is None:
        p = np.random.permutation(3)
    res = ''
    for i in range(3):
        if a[p[i]] == 0:
            continue
        n_spaces = 0
        if res != '':
            res += ' '
            n_spaces = 1
        if p[i] == 0:
            res += '{}x²'.format(get_signed_value(a[p[i]], without_plus=(res == ''), n_spaces=n_spaces))
        elif p[i] == 1:
            res += '{}x'.format(get_signed_value(a[p[i]], without_plus=(res == ''), n_spaces=n_spaces))
        else:
            res += '{}'.format(get_signed_value(a[p[i]], without_plus=(res == ''), show_one=True, n_spaces=n_spaces))
    return res
    
    
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
               '-(-{}) - {}'.format(a, b),
               '-(-{}) + (-{})'.format(a, b),
               '-(-{}) - (-{})'.format(a, b)]
        res = np.random.choice(all, 1)[0]
        return 'Вычисли: {}'.format(res), '{}'.format(get_str_value(eval(res), n=5))
    elif id <= 4:
        l, r = -9, 10
        if id == 4:
            l, r = -5, 5
        def get_coefficient():
            if np.random.rand() < 0.2:
                return np.random.choice([-1, 1])
            return np.random.randint(l, r)
        a = [get_coefficient(), get_coefficient(), np.random.randint(l, r)]
        while a[0] == 0:
            a[0] = get_coefficient()
        res = get_square_equation(a)
        if id == 3:
            return 'Последовательно выпиши три числа: коэффициенты <b>a, b, c</b> квадратного уравнения.\n\n{} = 0'.format(res), \
                   '{}, {}, {}'.format(get_str_value(a[0], n=5), get_str_value(a[1], n=5), get_str_value(a[2], n=5))
        else:
            D = a[1] ** 2 - 4 * a[0] * a[2]
            roots = 2
            if D == 0:
                roots = 1
            elif D < 0:
                roots = 0
            return 'Последовательно выпиши два числа: дискриминант и количество различных корней квадратного уравнения.\n\n{} = 0'.format(res), \
                   '{}, {}'.format(get_str_value(D, n=5), get_str_value(roots, n=5))
    elif id == 5:
        max_sqrt_d = 15
        if np.random.random() < 0.15:
            while True:
                a = [np.random.randint(-5, 6), np.random.randint(-15, 16), np.random.randint(-20, 20)]
                D = a[1] * a[1] - 4 * a[0] * a[2]
                if D < 0:
                    break
        else:
            while True:
                x1 = np.random.randint(-15, 16)
                x2 = np.random.randint(-15, 16)
                if abs(x1 - x2) <= max_sqrt_d:
                    break
            a = [1, -x1 - x2, x1 * x2]
            D = a[1] * a[1] - 4 * a[0] * a[2]
        while True:
            coef = np.random.choice([0.1, 0.5, 1, 2, 3, 4, 5, -0.1, -0.5, -1, -2, -3, -4, -5])
            if is_equal(abs(coef), 0.5) and D % 4 != 0 and D * 25 > max_sqrt_d * max_sqrt_d:
                continue
            if abs(a[1] * coef) <= 100 and D * coef * coef <= max_sqrt_d * max_sqrt_d:
                break
            
            
        a[0] *= coef
        a[1] *= coef
        a[2] *= coef
        D *= coef * coef
        res = get_square_equation(a)
        ans = 's '
        if D < 0:
            ans += '0 корней'
        elif D == 0:
            ans += '1 корень, x = {}'.format(get_str_value(x1))
        else:
            if x1 > x2:
                x1, x2 = x2, x1
            ans += '2 корня, x₁ = {}, x₂ = {}'.format(get_str_value(x1), get_str_value(x2))
        return 'Последовательно выпиши количество различных корней квадратного уравнения и сами корни.\n\n{} = 0\n\nИспользуй тот факт, что дискриминант D = {}'.format(res, get_str_value(D)), ans

        
def get_question(test):
    ids = [question.question_id for question in test.questions]
    id = np.random.choice(ids, 1)[0]
    return get_question_by_id(id)
