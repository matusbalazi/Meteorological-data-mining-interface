import mysql.connector as mysql
from io import BytesIO
from PIL import Image
import credentials

def connect_to_database():
    db_connection = mysql.connect(host=credentials.server_host_ip, database=credentials.database_name,
                                  user=credentials.database_user, password=credentials.database_password)
    return db_connection

def get_locations():
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

        print(result_sql_query_area_images)
        print(result_sql_query_city_images)
        print(result_sql_query_city_images_data)
        print(result_sql_query_city_data)
        print(areas)
        print(cities)

        return areas, cities

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()

    return locations, cities

def retrieve_image_from_database(image_id):
    db_connection = connect_to_database()

    cursor = db_connection.cursor()

    try:
        sql_select_query = "SELECT image FROM radar_images WHERE id = %s"
        data = (image_id,)

        cursor.execute(sql_select_query, data)

        result = cursor.fetchone()

        if result is not None:
            image_data = result[0]

            print(image_data)

        else:
            print("The image with the given ID was not found")

    except mysql.Error as error:
        print(f"Error loading image from database: {error}")

    finally:
        cursor.close()
        db_connection.close()