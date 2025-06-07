class Meetings:
    def __init__(self, venue, date, time):
        self.venue = venue
        self.date = date
        self.time = time

    def __str__(self):
        return self.venue


class RegisterChama:
    def __init__(self, first_name, last_name, name_of_chama, phone_number, email, id_number, county, password):
        self.first_name = first_name
        self.last_name = last_name
        self.name_of_chama = name_of_chama
        self.phone_number = phone_number
        self.email = email
        self.id_number = id_number
        self.county = county
        self.password = password

    def __str__(self):
        return self.name_of_chama


class SignUp:
    def __init__(self, first_name, last_name, phone_number, email, name_of_chama, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.name_of_chama = name_of_chama
        self.password = password

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Article:
    def __init__(self, title, headline, link, image):
        self.title = title
        self.headline = headline
        self.link = link
        self.image = image

    def __str__(self):
        return self.title