import db_operations
from flask_cors import CORS
from flask import Flask, jsonify, send_file, request
import os
import json
import shutil
from urllib.request import urlopen, pathname2url
from pathlib import Path
app = Flask(__name__)
CORS(app)


# 1
@app.route('/api/available_locations', methods=['GET'])
def api_get_available_locations():
    areas, cities = db_operations.get_available_locations()
    return jsonify({'areas': areas, 'cities': cities})


# 2 a,b,c
@app.route('/api/exist_records/<string:location>', methods=['GET'])
def api_exist_records(location):
    exist_weather_images, exist_weather_data, exist_weather_images_with_data = db_operations.find_record_in_db(location)
    return jsonify({'exist_weather_images': exist_weather_images, 'exist_weather_data': exist_weather_data,
                    'exist_weather_images_with_data': exist_weather_images_with_data})


# 3 a,c
@app.route('/api/available_layers/<string:location>', methods=['GET'])
def api_get_available_layers(location):
    layers_weather_data_id_null, layers_weather_data_id_not_null = db_operations.get_available_layers(location)
    return jsonify({'layers': layers_weather_data_id_null,
                    'layers_with_data': layers_weather_data_id_not_null})


# 4 a,b,c
@app.route('/api/available_dates/<string:location>/<string:layer>', methods=['GET'])
def api_get_available_dates(location, layer):
    range_data_weather_data_id_null, range_data_weather_data, range_data_weather_data_id_not_null = db_operations.get_available_dates(
        location, layer)
    return jsonify({'range_data_weather_data_id_null': range_data_weather_data_id_null,
                    'range_data_weather_data': range_data_weather_data,
                    'range_data_weather_data_id_not_null': range_data_weather_data_id_not_null})


# 5 a
@app.route('/api/weather_images/<string:location>/<string:layer>/<string:date_from>/<string:date_to>', methods=['GET'])
def api_get_weather_images(location, layer, date_from, date_to):
    weather_images = db_operations.get_weather_images(location, layer, date_from, date_to)
    temp_dir = './temp_images_directory'
    os.makedirs(temp_dir, exist_ok=True)

    for image_info in weather_images:
        date, image_path = image_info

        # Download the image from the provided path using urllib
        image_path = Path(os.path.join(Path(os.getcwd()).parent, "Meteorological-data-mining", image_path))
        image_url = image_path.as_uri()
        with urlopen(image_url) as response:
            # Save the image file in the temporary directory
            date_folder = os.path.join(temp_dir, date.replace(':', '_').replace(' ', '_'))
            os.makedirs(date_folder, exist_ok=True)

            image_file_path = os.path.join(date_folder, layer + '.jpg')
            with open(image_file_path, 'wb') as image_file:
                image_file.write(response.read())

    # Create a zip file containing all image folders
    zip_file_path = './weather_images.zip'  # Replace with the actual path
    shutil.make_archive(os.path.normpath(zip_file_path[:-4]), 'zip', os.path.normpath(temp_dir))

    # Clean up temporary image directory
    shutil.rmtree(temp_dir)

    # Send the zip file for download
    return send_file(zip_file_path, as_attachment=True, download_name=f'weather_images_{location}.zip')


# 5 b
@app.route('/api/weather_data/<string:location>/<string:weather_data_types>/<string:date_from>/<string:date_to>',
           methods=['GET'])
def api_get_weather_data(location, weather_data_types, date_from, date_to):
    weather_data = db_operations.get_weather_data(location, weather_data_types, date_from, date_to)
    temp_dir = './temp_directory'
    os.makedirs(temp_dir, exist_ok=True)

    # Save each record as a separate JSON file
    for record in weather_data:
        date_folder = temp_dir + "/" + record['date'].replace(':', '_').replace(' ', '_')
        os.makedirs(date_folder, exist_ok=True)

        json_file_path = os.path.join(date_folder, 'data.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(record, json_file, indent=2)

    # Create a zip file containing all folders
    zip_file_path = './output.zip'
    shutil.make_archive(zip_file_path[:-4], 'zip', temp_dir)

    # Clean up temporary directory
    shutil.rmtree(temp_dir)

    # Send the zip file for download
    return send_file(zip_file_path, as_attachment=True, download_name=f'weather_data_{location}.zip')


# 5 c
@app.route(
    '/api/weather_images_and_data/<string:location>/<string:layer>/<string:weather_data_types>/<string:date_from>/<string:date_to>',
    methods=['GET'])
def api_get_weather_images_and_data(location, layer, weather_data_types, date_from, date_to):
    weather_images_and_data = db_operations.get_weather_images_and_data(location, layer, weather_data_types, date_from,
                                                                        date_to)
    temp_dir = './temp_images_and_data_directory'
    os.makedirs(temp_dir, exist_ok=True)

    for record in weather_images_and_data:
        date = record['date']
        image_path = record['image']
        data = {key.rstrip(','): value for key, value in record.items() if key not in ['date', 'image']}
        data['date'] = date

        # Download the image
        image_path = Path(os.path.join(Path(os.getcwd()).parent, "Meteorological-data-mining", image_path))
        image_url = image_path.as_uri()
        with urlopen(image_url) as response:
            # Save the image file in the temporary directory
            date_folder = os.path.join(temp_dir, date.replace(':', '_').replace(' ', '_'))
            os.makedirs(date_folder, exist_ok=True)

            image_file_path = os.path.join(date_folder, layer + '.jpg')
            with open(image_file_path, 'wb') as image_file:
                image_file.write(response.read())

            # Save the data as a JSON file in the same folder
            data_file_path = os.path.join(date_folder, 'data.json')
            with open(data_file_path, 'w') as data_file:
                json.dump(data, data_file, indent=2)

    # Create a zip file containing all image and data folders
    zip_file_path = f'./weather_images_and_data_{location}.zip'  # Replace with the actual path
    shutil.make_archive(os.path.normpath(zip_file_path[:-4]), 'zip', os.path.normpath(temp_dir))

    # Clean up temporary directory
    shutil.rmtree(temp_dir)

    # Send the zip file for download
    return send_file(zip_file_path, as_attachment=True, download_name=f'weather_images_and_data_{location}.zip')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    main()
