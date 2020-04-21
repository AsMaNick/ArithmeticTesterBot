def get_name(user):
    res = ''
    if user.first_name:
        res += user.first_name
    if user.last_name:
        if res != '':
            res += ' '
        res += user.last_name
    return res
    
    
def parse_int_list(s):
    res = []
    last = 0
    started = False
    for c in s:
        if '0' <= c <= '9':
            last = last * 10 + ord(c) - ord('0')
            started = True
        else:
            if started:
                res.append(last)
                last = 0
                started = False
    if started:
        res.append(last)
    return res
    

def parse_float_list(s):
    res = []
    last = 0
    started = False
    pos_after_dot = 0
    sign = 0
    for c in s:
        if '0' <= c <= '9':
            started = True
            if sign == 0:
                sign = 1
            if pos_after_dot == 0:
                last = last * 10 + ord(c) - ord('0')
            else:
                last = last + (ord(c) - ord('0')) / (10 ** pos_after_dot)
                pos_after_dot += 1
        else:
            if started and c == '.' and pos_after_dot == 0:
                pos_after_dot = 1
            elif started:
                res.append(sign * last)
                last = 0
                sign = 0
                started = False
                pos_after_dot = 0
            if c == '-':
                sign = -1
    if started:
        res.append(sign * last)
    return res

    
def unique_elements(a):
    return sorted(list(set(a)))

    
def is_equal(x, y):
    if isinstance(x, list):
        if isinstance(y, list):
            if len(x) != len(y):
                return False
            for a, b in zip(x, y):
                if not is_equal(a, b):
                    return False
            return True
        return False
    return abs(x - y) <= 1e-6
    
    
def get_delta_time(t1, t2):
    return float('{:.2f'.format(t2 - t1))
    

def round_to(x, n):
    return float('{:.{}f}'.format(x, n))

    
def get_str_value(x, n=8):
    x = round_to(x, n)
    if is_equal(x, int(x)):
        return str(int(x))
    return str(x)
    
    
def get_signed_value(x, without_plus=False, show_one=False, show_zero=True, n_spaces=0):
    if not show_zero and abs(x) <= 1e-7:
        return ''
    spaces = ' ' * n_spaces
    if not show_one:
        if is_equal(x, 1):
            if without_plus:
                return ''
            return '+' + spaces
        if is_equal(x, -1):
            return '-' + spaces
    res = get_str_value(x)
    if res[0] == '-':
        return '-' + spaces + res[1:]
    if without_plus:
        return res
    return '+' + spaces + res
    
    
def str_time(t):
    t = int(t)
    if t >= 3600:
        return '{}:{:02d}:{:02d}'.format(t // 3600, (t % 3600) // 60, (t % 3600) % 60)
    return '{:02d}:{:02d}'.format(t // 60, t % 60)
    
    
def get_text_comment(p):
    p *= 100
    if p < 50:
        return 'Ты можешь лучше, будь внимательнее!'
    elif p < 60:
        return 'Ты имеешь представление об этой теме, улучшай свой результат!'
    elif p < 75:
        return 'Неплохо, но еще есть куда стремиться...'
    elif p < 90:
        return 'Хорошо! У тебя получается!'
    return 'Отлично, ты молодец :)'
    
    
def check_answer(correct, answer):
    return is_equal(parse_float_list(correct), parse_float_list(answer))
