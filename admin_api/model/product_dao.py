from sqlalchemy import text

class ProductDao:
    def __init__(self, database):
        self.db = database

    def get_country_of_origin(self, country_id):
        row = self.db.execute(text(
            """
            SELECT
                id,
                name
            FROM country_of_origins
            WHERE id = :country_id
            """), {'country_id':country_id}).fetchone()

        return {
            'country_id'   : row['id'],
            'country_name' : row['name']
        } if row else None
