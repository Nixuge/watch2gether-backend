import random

ALPHABET_NUMBERS = "0123456789abcdefghijklmnopqrstuvwxyz"

def random_string(chars: str, length: int):
    return ''.join(random.choice(chars) for _ in range(length))