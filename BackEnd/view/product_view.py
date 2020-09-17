from flask import jsonify

from flask.views import MethodView

class CountryOfOriginView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self, country_id):
        country_of_origin = self.service.get_country_of_origin(country_id)

        return jsonify(country_of_origin), 200
