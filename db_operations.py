import mysql.connector as mysql
from io import BytesIO
from PIL import Image
import credentials

def connect_to_database():
    db_connection = mysql.connect(host=credentials.server_host_ip, database=credentials.database_name,
                                  user=credentials.database_user, password=credentials.database_password)
    return db_connection

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