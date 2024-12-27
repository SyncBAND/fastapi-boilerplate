from faker import Faker

fake = Faker()


def create_fake_user():
    """Create a dictionary with fake user data."""
    password = fake.password(length=12)
    return {
        "email": fake.email(),
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "password": password,
        "confirm_password": password,
    }
