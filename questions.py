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
    elif 6 <= id and id <= 11:
        def get_all_primes(n):
            is_prime = [True for i in range(n)]
            res = []
            for i in range(2, n):
                if is_prime[i]:
                    res.append(i)
                    for j in range(2 * i, n, i):
                        is_prime[j] = False
            return res
        if id == 6:
            mods = get_all_primes(51)
            probs = np.array(mods) ** 0.5
            probs /= np.sum(probs)
            mod = np.random.choice(mods, p=probs)
            a = np.random.randint(mod)
            b = np.random.randint(mod)
            return f'Вычисли {a} + {b} в поле по модулю {mod}', (a + b) % mod
        elif id == 7:
            mods = get_all_primes(51)
            probs = np.array(mods) ** 0.5
            probs /= np.sum(probs)
            mod = np.random.choice(mods, p=probs)
            if np.random.rand() < 0.1:
                a = np.random.randint(1, mod)
                return f'Вычисли {-a} в поле по модулю {mod}', (-a) % mod
            a = np.random.randint(mod)
            b = np.random.randint(mod)
            return f'Вычисли {a} - {b} в поле по модулю {mod}', (a - b) % mod
        elif id == 8:
            mods = get_all_primes(14)
            probs = np.array(mods) ** 0.5
            probs /= np.sum(probs)
            mod = np.random.choice(mods, p=probs)
            a = np.random.randint(mod)
            b = np.random.randint(mod)
            return f'Вычисли {a} * {b} в поле по модулю {mod}', (a * b) % mod
        else:
            def inverse(x, mod):
                def power(x, n, mod):
                    res = 1
                    while n > 0:
                        if n % 2 == 1:
                            res = (res * x) % mod
                        x = (x * x) % mod
                        n //= 2
                    return res
                return power(x, mod - 2, mod)
            mods = get_all_primes(12)
            probs = np.array(mods) ** 1.0
            probs /= np.sum(probs)
            mod = np.random.choice(mods, p=probs)
            if id == 9:
                a = np.random.randint(1, mod)
                return f'Вычисли обратный элемент к числу {a} в поле по модулю {mod}', inverse(a, mod)
            elif id == 10:
                a = np.random.randint(mod)
                b = np.random.randint(1, mod)
                return f'Вычисли {a} / {b} в поле по модулю {mod}', (a * inverse(b, mod)) % mod
            else:
                a = np.random.randint(mod)
                b = np.random.randint(1, mod)
                c = np.random.randint(mod)
                d = np.random.randint(1, mod)
                sign = np.random.choice(['+', '-'])
                return f'Вычисли {a}/{b} {sign} {c}/{d} в поле по модулю {mod}', eval(f'a * inverse(b, mod) {sign} c * inverse(d, mod)') % mod
def get_question(test):
    ids = [question.question_id for question in test.questions]
    id = np.random.choice(ids, 1)[0]
    return get_question_by_id(id)
