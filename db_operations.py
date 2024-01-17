import mysql.connector as mysql
import credentials

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
        sql_query_exist_weather_images = "SELECT * FROM radar_images WHERE location = %s AND weather_data_id IS NULL"
        data = (location,)
        cursor.execute(sql_query_exist_weather_images, data)
        result_sql_query_exist_weather_images = cursor.fetchall()

        if len(result_sql_query_exist_weather_images):
            exist_weather_images = True

        sql_query_exist_weather_data = "SELECT * FROM weather_info WHERE city = %s"
        data = (location,)
        cursor.execute(sql_query_exist_weather_data, data)
        result_sql_query_exist_weather_data = cursor.fetchall()

        if len(result_sql_query_exist_weather_data):
            exist_weather_data = True

        sql_query_exist_weather_images_with_data = "SELECT * FROM radar_images WHERE location = %s AND weather_data_id IS NOT NULL"
        data = (location,)
        cursor.execute(sql_query_exist_weather_images_with_data, data)
        result_sql_query_exist_weather_images_with_data = cursor.fetchall()

        if len(result_sql_query_exist_weather_images_with_data):
            exist_weather_images_with_data = True

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