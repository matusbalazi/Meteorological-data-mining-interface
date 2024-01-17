import db_operations

def main():
    print(db_operations.get_available_locations())
    print(db_operations.find_record_in_db("Kosice"))
    print(db_operations.get_available_layers("Bardejov"))
    print(db_operations.get_available_dates("Kosice", "AIRMASS_RGB"))

if __name__ == '__main__':
    main()