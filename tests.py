from utils import *


def test_is_equal():
    assert(is_equal(0, 0))
    assert(is_equal(0, -0))
    assert(is_equal(12.3, 12.3))
    assert(not is_equal(12.3, 12.34))
    assert(is_equal([1, 2.31, -1.23], [1, 2.310, -1.230]))
    assert(not is_equal([1, 2.31, -1.23], [1, -2.310, -1.230]))
    assert(not is_equal([1, 2.31, -1.23], [1, 2.31]))
    
    
    
def test_parse_float_list():
    assert(is_equal(parse_float_list(''), []))
    assert(is_equal(parse_float_list('a b . '), []))
    assert(is_equal(parse_float_list('1 2 3, 4.5, 13.3, 1, 0; 123.1123'), [1, 2, 3, 4.5, 13.3, 1, 0, 123.1123]))
    assert(is_equal(parse_float_list('-1 -2 -3, -4.5, -13.3, -1, -0; -123.1123'), [-1, -2, -3, -4.5, -13.3, -1, 0, -123.1123]))
    assert(is_equal(parse_float_list('-1 2 -3, 4.5, 13.3, -1, 0; -123.1123'), [-1, 2, -3, 4.5, 13.3, -1, 0, -123.1123]))
    
    
def test_get_str_value():
    assert(get_str_value(1.0000000000001) == '1')
    assert(get_str_value(-1.000000000001) == '-1')
    assert(get_str_value(0.0000000000001) == '0')
    assert(get_str_value(-0.000000000001) == '0')
    assert(get_str_value(123.45678) == '123.45678')
    assert(get_str_value(-123.4567) == '-123.4567')
    
    
test_is_equal()
test_parse_float_list()
test_get_str_value()