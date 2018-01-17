from django.core.validators import validate_email
import random, string


def is_email_valid(email):
    try:
        validate_email(email)
        return True
    except:
        return False


def random_string(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
