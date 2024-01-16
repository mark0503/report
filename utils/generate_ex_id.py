from enum import Enum
import random
import uuid


class ExIdType(Enum):
    # Обычный uuid4
    BASE_ID = '1'
    # Длинный uuid4 * 4
    LONG_ID = '2'
    # Числовой id
    DIGIT_ID = '3'


def generate_base_id():
    return uuid.uuid4().__str__().replace('-', '')

def generate_long_id():
    long_id = ''
    for _ in range(4):
        long_id += uuid.uuid4().__str__().replace('-', '')
    return long_id

def generate_digit_id():
    min_value = 1000000
    max_value = 2500000
    random_number = random.randint(min_value, max_value)
    random_number_string = str(random_number)
    return random_number_string

def generate_id_of_type(type_id: str):
    if type_id == '1':
        return generate_base_id()
    elif type_id == '2':
        return generate_long_id()
    else:
        return generate_digit_id()