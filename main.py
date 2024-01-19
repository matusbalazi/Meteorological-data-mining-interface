from flask import Flask, jsonify, request
import db_operations

app = Flask(__name__)


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
    return jsonify({'layers_weather_data_id_null': layers_weather_data_id_null,
                    'layers_weather_data_id_not_null': layers_weather_data_id_not_null})


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
    return jsonify({'weather_images': weather_images})


# 5 b
@app.route('/api/weather_data/<string:location>/<string:weather_data_types>/<string:date_from>/<string:date_to>',
           methods=['GET'])
def api_get_weather_data(location, weather_data_types, date_from, date_to):
    weather_data = db_operations.get_weather_data(location, weather_data_types, date_from, date_to)
    return jsonify({'weather_data': weather_data})


# 5 c
@app.route(
    '/api/weather_images_and_data/<string:location>/<string:layer>/<string:weather_data_types>/<string:date_from>/<string:date_to>',
    methods=['GET'])
def api_get_weather_images_and_data(location, layer, weather_data_types, date_from, date_to):
    weather_images_and_data = db_operations.get_weather_images_and_data(location, layer, weather_data_types, date_from,
                                                                        date_to)
    return jsonify({'weather_images_and_data': weather_images_and_data})


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

    app.run(debug=True)


if __name__ == '__main__':
    main()
