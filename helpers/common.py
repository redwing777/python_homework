import random
import string


def password_gen(lowercase=8, uppercase=3, special=3, digits=2):
    uppercase = "".join(random.choice(string.ascii_uppercase) for i in range(uppercase)) if uppercase else ''
    special = "".join(random.choice(string.punctuation.replace("'", "").replace('"', '')) for i in range(special)) if special else ''
    digits = "".join(random.choice(string.digits) for i in range(digits)) if digits else ''
    return f'{"".join(random.choice(string.ascii_lowercase) for i in range(lowercase))}{uppercase}{special}{digits}'
