import mysql.connector as mysql
import credentials
import datetime
import decimal


def connect_to_database():
    db_connection = mysql.connect(host=credentials.server_host_ip, database=credentials.database_name,
                                  user=credentials.database_user, password=credentials.database_password)
    return db_connection


def get_available_locations():
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    areas = []
    cities = []

    try:
        sql_query_area_images = "SELECT DISTINCT location FROM radar_images WHERE location_type = %s ORDER BY location ASC"
        data = ("area",)
        cursor.execute(sql_query_area_images, data)
        result_sql_query_area_images = cursor.fetchall()

        sql_query_city_images = "SELECT DISTINCT location FROM radar_images WHERE location_type = %s AND weather_data_id IS NULL ORDER BY location ASC"
        data = ("city",)
        cursor.execute(sql_query_city_images, data)
        result_sql_query_city_images = cursor.fetchall()

        sql_query_city_images_data = "SELECT DISTINCT location FROM radar_images WHERE location_type = %s AND weather_data_id IS NOT NULL ORDER BY location ASC"
        data = ("city",)
        cursor.execute(sql_query_city_images_data, data)
        result_sql_query_city_images_data = cursor.fetchall()

        sql_query_city_data = "SELECT DISTINCT city FROM weather_info ORDER BY city ASC"
        cursor.execute(sql_query_city_data)
        result_sql_query_city_data = cursor.fetchall()

        for i in result_sql_query_area_images:
            areas.append(i[0])

        for i in result_sql_query_city_images:
            cities.append(i[0])

        for i in result_sql_query_city_images_data:
            if i[0] not in cities:
                cities.append(i[0])

        for i in result_sql_query_city_data:
            if i[0] not in cities:
                cities.append(i[0])

        areas.sort()
        cities.sort()

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()

    return areas, cities


def find_record_in_db(location):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    exist_weather_images = False
    exist_weather_data = False
    exist_weather_images_with_data = False

    try:
        sql_query_exist_weather_images_with_data = "SELECT * FROM radar_images WHERE location = %s AND weather_data_id IS NOT NULL"
        data = (location,)
        cursor.execute(sql_query_exist_weather_images_with_data, data)
        result_sql_query_exist_weather_images_with_data = cursor.fetchall()

        if not result_sql_query_exist_weather_images_with_data:
            exist_weather_images_with_data = False
        else:
            exist_weather_images_with_data = True
            exist_weather_images = True
            exist_weather_data = True

        if (exist_weather_images_with_data == False):
            sql_query_exist_weather_images = "SELECT * FROM radar_images WHERE location = %s"
            data = (location,)
            cursor.execute(sql_query_exist_weather_images, data)
            result_sql_query_exist_weather_images = cursor.fetchall()

            if not result_sql_query_exist_weather_images:
                exist_weather_images = False
            else:
                exist_weather_images = True

            sql_query_exist_weather_data = "SELECT * FROM weather_info WHERE city = %s"
            data = (location,)
            cursor.execute(sql_query_exist_weather_data, data)
            result_sql_query_exist_weather_data = cursor.fetchall()

            if not result_sql_query_exist_weather_data:
                exist_weather_data = False
            else:
                exist_weather_data = True

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()

    return exist_weather_images, exist_weather_data, exist_weather_images_with_data


def get_available_layers(location):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    layers_weather_data_id_null = []
    layers_weather_data_id_not_null = []

    try:
        sql_query_weather_data_id_null = "SELECT DISTINCT layer FROM radar_images WHERE location = %s AND weather_data_id IS NULL ORDER BY layer ASC"
        data = (location,)
        cursor.execute(sql_query_weather_data_id_null, data)
        result_sql_query_weather_data_id_null = cursor.fetchall()

        sql_query_weather_data_id_not_null = "SELECT DISTINCT layer FROM radar_images WHERE location = %s AND weather_data_id IS NOT NULL ORDER BY layer ASC"
        data = (location,)
        cursor.execute(sql_query_weather_data_id_not_null, data)
        result_sql_query_weather_data_id_not_null = cursor.fetchall()

        for i in result_sql_query_weather_data_id_null:
            layers_weather_data_id_null.append(i[0])

        for i in result_sql_query_weather_data_id_not_null:
            layers_weather_data_id_not_null.append(i[0])

        layers_weather_data_id_null.sort()
        layers_weather_data_id_not_null.sort()

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()

    return layers_weather_data_id_null, layers_weather_data_id_not_null


def get_available_dates(location, layer):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    range_data_weather_data_id_null = []
    range_data_weather_data_id_not_null = []
    range_data_weather_data = []

    try:
        sql_query_dates_weather_data_id_null = "SELECT MIN(date), MAX(date) FROM radar_images WHERE location = %s AND layer = %s AND weather_data_id IS NULL"
        data = (location, layer,)
        cursor.execute(sql_query_dates_weather_data_id_null, data)
        result_sql_query_dates_weather_data_id_null = cursor.fetchall()

        sql_query_dates_weather_data_id_not_null = "SELECT MIN(date), MAX(date) FROM radar_images WHERE location = %s AND layer = %s AND weather_data_id IS NOT NULL"
        data = (location, layer,)
        cursor.execute(sql_query_dates_weather_data_id_not_null, data)
        result_sql_query_dates_weather_data_id_not_null = cursor.fetchall()

        sql_query_dates_weather_data = "SELECT MIN(time_of_data_calc), MAX(time_of_data_calc) FROM weather_info WHERE city = %s"
        data = (location,)
        cursor.execute(sql_query_dates_weather_data, data)
        result_sql_query_dates_weather_data = cursor.fetchall()

        if all(result_sql_query_dates_weather_data_id_null[0]) > 0:
            range_data_weather_data_id_null.append(
                datetime.datetime.strftime(result_sql_query_dates_weather_data_id_null[0][0], "%d.%m.%Y"))
            range_data_weather_data_id_null.append(
                datetime.datetime.strftime(result_sql_query_dates_weather_data_id_null[0][1], "%d.%m.%Y"))

        if all(result_sql_query_dates_weather_data_id_not_null[0]) > 0:
            range_data_weather_data_id_not_null.append(
                datetime.datetime.strftime(result_sql_query_dates_weather_data_id_not_null[0][0], "%d.%m.%Y"))
            range_data_weather_data_id_not_null.append(
                datetime.datetime.strftime(result_sql_query_dates_weather_data_id_not_null[0][1], "%d.%m.%Y"))

        if all(result_sql_query_dates_weather_data[0]) > 0:
            range_data_weather_data.append(
                datetime.datetime.strftime(result_sql_query_dates_weather_data[0][0], "%d.%m.%Y"))
            range_data_weather_data.append(
                datetime.datetime.strftime(result_sql_query_dates_weather_data[0][1], "%d.%m.%Y"))

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()

    return range_data_weather_data_id_null, range_data_weather_data, range_data_weather_data_id_not_null


def get_weather_images(location, layer, date_from, date_to):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    weather_images = []

    try:
        sql_query_weather_images = "SELECT date, image FROM radar_images WHERE location = %s AND layer = %s AND date BETWEEN %s AND %s"
        data = (location, layer, date_from, date_to)
        cursor.execute(sql_query_weather_images, data)
        result_sql_query_weather_images = cursor.fetchall()

        if len(result_sql_query_weather_images) > 0:
            for i in result_sql_query_weather_images:
                weather_item = []
                weather_item.append(datetime.datetime.strftime(i[0], "%d.%m.%Y"))
                weather_item.append(i[1])
                weather_images.append(weather_item)

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()

    return weather_images


def get_weather_data(location, weather_data_types, date_from, date_to):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    weather_data = []

    try:
        sql_query_weather_data = "SELECT time_of_data_calc, " + weather_data_types + " FROM weather_info WHERE city = %s AND time_of_data_calc BETWEEN %s AND %s"
        data = (location, date_from, date_to)
        cursor.execute(sql_query_weather_data, data)
        result_sql_query_weather_data = cursor.fetchall()

        if len(result_sql_query_weather_data) > 0:
            for i in result_sql_query_weather_data:
                weather_item = []
                weather_item.append(datetime.datetime.strftime(i[0], "%d.%m.%Y"))
                for j in range(1, len(list(weather_data_types.split(" "))) + 1):
                    if type(i[j]) is decimal.Decimal:
                        weather_item.append(float(i[j]))
                    else:
                        weather_item.append(str(i[j]))
                weather_data.append(weather_item)

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()

    return weather_data


def get_weather_images_and_data(location, layer, weather_data_types, date_from, date_to):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    weather_images_and_data = []

    try:
        sql_query_weather_images_and_data = "SELECT date, image, " + weather_data_types + " FROM radar_images JOIN weather_info ON radar_images.weather_data_id = weather_info.id WHERE location = %s AND layer = %s AND date BETWEEN %s AND %s"
        data = (location, layer, date_from, date_to)
        cursor.execute(sql_query_weather_images_and_data, data)
        result_sql_query_weather_images_and_data = cursor.fetchall()

        if len(result_sql_query_weather_images_and_data) > 0:
            for i in result_sql_query_weather_images_and_data:
                weather_item = []
                weather_item.append(datetime.datetime.strftime(i[0], "%d.%m.%Y"))
                weather_item.append(i[1])
                for j in range(2, len(list(weather_data_types.split(" "))) + 1):
                    if type(i[j]) is decimal.Decimal:
                        weather_item.append(float(i[j]))
                    else:
                        weather_item.append(str(i[j]))
                weather_images_and_data.append(weather_item)

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()

    return weather_images_and_data
