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
    

def unique_elements(a):
    return sorted(list(set(a)))

    
def is_equal(x, y):
    return abs(x - y) <= 1e-6
    
    
def get_delta_time(t1, t2):
    return float('{:.2f'.format(t2 - t1))
    

def round_to(x, n):
    return float('{:.{}f}'.format(x, n))

    
def get_str_value(x, n=10):
    if is_equal(x, int(x)):
        return str(int(x))
    return str(round_to(x, n))
    
    
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