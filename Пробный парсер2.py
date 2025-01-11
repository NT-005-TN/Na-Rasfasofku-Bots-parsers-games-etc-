import googlemaps

def find_organization_info(name):
    api_key = "ВАШ_API_KEY"
    gmaps = googlemaps.Client(key=api_key)

    result = gmaps.places(query=name)

    if result['status']!= 'OK':
        print("Организация не найдена")
        return

    place_id = result['results'][0]['place_id']
    place_info = gmaps.place(place_id)

    address = place_info['result']['formatted_address']
    city = None
    for component in place_info['result']['address_components']:
        if 'locality' in component['types']:
            city = component['long_name']
            break

    latitude = place_info['result']['geometry']['location']['lat']
    longitude = place_info['result']['geometry']['location']['lng']

    print(f"Адрес: {address}")
    print(f"Город: {city}")
    print(f"Координаты: {latitude}, {longitude}")

name = input("Введите название организации: ")
find_organization_info(name)
