import base62
import random

def hashing(keyword):
    byte_array = keyword.encode('utf-8')
    new_word = base62.encodebytes(byte_array)
    
    short_list = list(new_word)
    q = random.sample(short_list, k=5)
    short = ''.join(q)
    
    return short