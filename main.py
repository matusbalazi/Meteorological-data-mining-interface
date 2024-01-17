import db_operations

def main():
    print(db_operations.get_available_locations())
    print(db_operations.find_record_in_db("Kosice"))
    print(db_operations.get_available_layers("Bardejov"))
    print(db_operations.get_available_dates("Kosice", "AIRMASS_RGB"))
    print(db_operations.get_weather_images("SLOVAKIA", "AIRMASS_RGB", "20-01-23", "31-01-24"))

if __name__ == '__main__':
    main()