import random
import string


def generate_alphanumeric_captcha(challenge=None, **kwargs):
    """
     Generates a random alphanumeric CAPTCHA consisting of digits and uppercase letters.

     This function returns a tuple (question, answer) as required by django-simple-captcha.
     The CAPTCHA is between 4 and 6 characters long, with at least 2 digits and the rest being a mix
     of digits and uppercase letters. The returned answer is in both uppercase and lowercase formats.

     Parameters:
     - challenge: Not used in this implementation, but included for compatibility with django-simple-captcha.
     - kwargs: Additional keyword arguments that are not used in this function but may be passed for compatibility.

     Returns:
     - A tuple (question, answer), where 'question' is the answer in lowercase and 'answer' is in uppercase.
     """

    captcha_length = random.randint(4, 6)

    captcha = [random.choice(string.digits) for _ in range(2)]
    captcha += [random.choice(string.ascii_uppercase + string.digits) for _ in range(captcha_length - 2)]
    random.shuffle(captcha)
    answer = ''.join(captcha)

    return answer.upper(), answer.lower()

