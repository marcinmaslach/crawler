
class User_Filtr:

    def __init__(self, number_of_rooms, price_from, price_to, localization):
        self.number_of_rooms = number_of_rooms
        self.price_from = price_from
        self.price_to = price_to
        self.localization = localization

    def make_taget_url(self):

        target_url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bfilter_float_price%3Afrom%5D=" + str(self.price_from) + "&search%5Bfilter_float_price%3Ato%5D=" + str(self.price_to) + "&search%5Bfilter_enum_rooms%5D%5B0%5D=" + self.number_of_rooms + "&search%5Bdistrict_id%5D=" + self.localization

        return target_url

    def make_config_list(self):
        self.read_number_of_rooms()
        return [self.number_of_rooms, self.price_from, self.price_to, self.localization]
