from faker import Faker

fake = Faker()


def create_fake_mood():
    learning = fake.paragraph(nb_sentences=6, variable_nb_sentences=True)
    personal_note = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
    rating = fake.random_int(min=0, max=10)
    return {
        "learning": learning,
        "personal_note": personal_note,
        "rating": rating
    }
