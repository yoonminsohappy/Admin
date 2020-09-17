from flask import jsonify

def create_endpoints(app, services):
    product_service = services.product_service

    @app.route("/country_of_origin/<int:country_id>", methods=['GET'])
    def get_country_of_origin(country_id):
        country_of_origin = product_service.get_country_of_origin(country_id)

        return jsonify(country_of_origin), 200
