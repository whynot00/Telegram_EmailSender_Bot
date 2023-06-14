from geopy.distance import geodesic as geo
from geopy.geocoders import Nominatim

source = "город нижний Новгород, уЛ.Львоская,дом 55/3, 13"
list_prim = ["корп", "корпус", "г", "город", "ул", "улица", "д", "дом", "кв", "квартира", "к"]



def normalize_address(address):

    address_str = address.replace(",", " ").replace(".", " ").replace("-", " ").replace("/", " к ").split()
    for index, item in enumerate(address_str):
        if address_str[index].lower() in list_prim:
            address_str.remove(address_str[index])

    stirng_all = ""

    for element in address_str:
        stirng_all += f"{element.title()} "

    return stirng_all

def adress_check_true (adress):
    geolocator = Nominatim(user_agent="Tester")
    location_adress = geolocator.geocode(adress)
    if location_adress:
        return True
