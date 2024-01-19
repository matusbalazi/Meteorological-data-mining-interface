import db_operations


def main():
    # 1
    print(db_operations.get_available_locations())

    # 2 a,b,c
    print(db_operations.find_record_in_db("Kosice"))

    # 3 a,c
    print(db_operations.get_available_layers("Bardejov"))

    # 4 a,b,c
    print(db_operations.get_available_dates("Kosice", "AIRMASS_RGB"))

    # 5 a
    print(db_operations.get_weather_images("SLOVAKIA", "AIRMASS_RGB", "20-01-23", "31-01-24"))

    weather_data_types = ', '.join(["description", "temp_celsius", "wind_speed", "clouds"])

    # 5 b
    print(db_operations.get_weather_data("Kosice", weather_data_types, "20-01-23", "31-01-24"))

    # 5 c
    print(
        db_operations.get_weather_images_and_data("Kosice", "AIRMASS_RGB", weather_data_types, "20-01-23", "31-01-24"))


if __name__ == '__main__':
    main()
