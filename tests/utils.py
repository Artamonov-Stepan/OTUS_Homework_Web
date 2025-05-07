from faker import Faker
import random
import string

fake = Faker("en_US")
ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + "-_"


def generate_random_data():
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    password = fake.password(length=12)
    product_name = generate_random_string(min_length=1, max_length=100)
    tag_title = generate_random_string(min_length=1, max_length=100)
    model = generate_random_string(min_length=1, max_length=50)
    keyword = generate_random_string(
        min_length=5, max_length=15, allowed_chars=ALLOWED_CHARACTERS
    )

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "product_name": product_name,
        "tag_title": tag_title,
        "model": model,
        "keyword": keyword,
    }


def generate_random_string(min_length=1, max_length=255, allowed_chars=None):
    if allowed_chars is None:
        allowed_chars = string.printable.strip()
    else:
        allowed_chars = list(set(allowed_chars))

    length = random.randint(min_length, max_length)
    return "".join(random.choice(allowed_chars) for _ in range(length))
