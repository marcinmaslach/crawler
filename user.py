

class User:

    def __init__(self, number_of_rooms, price_from, price_to, localization):
        self.number_of_rooms = number_of_rooms
        self.price_from = price_from
        self.price_to = price_to
        self.localization = localization

    def read_number_of_rooms(self):

        if self.number_of_rooms in ["one", "two", "three", "four"]:
            pass
        elif self.number_of_rooms == "Kawalerka":
            self.number_of_rooms = "one"
        elif self.number_of_rooms == "2 pokoje":
            self.number_of_rooms = "two"
        elif self.number_of_rooms == "3 pokoje":
            self.number_of_rooms = "three"
        else:
            self.number_of_rooms = "four"

    def read_lokalization(self):
        lok = None

        if self.localization == "Krzyki":
            lok = "391"
        elif self.localization == "Fabryczna":
            lok = "393"
        elif self.localization == "Psie Pole":
            lok = "389"
        elif self.localization == "Śródmieście":
            lok = "387"
        elif self.localization == "Stare Miasto":
            lok = "385"

        return lok

    def make_taget_url(self):
        lok = self.read_lokalization()
        self.read_number_of_rooms()

        target_url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bfilter_float_price%3Afrom%5D=" + self.price_from + "&search%5Bfilter_float_price%3Ato%5D=" + self.price_to + "&search%5Bfilter_enum_rooms%5D%5B0%5D=" + self.number_of_rooms + "&search%5Bdistrict_id%5D=" + lok

        return target_url

    def make_config_list(self):
        self.read_number_of_rooms()
        return [self.number_of_rooms, self.price_from, self.price_to, self.localization]
