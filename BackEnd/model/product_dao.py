from sqlalchemy import text

# 작성자: 김태수
# 작성일: 2020.09.17.목
# Product와 연결된 Class
class ProductDao:
    def __init__(self, database):
        self.db = database

    # 작성자: 김태수
    # 작성일: 2020.09.17.목
    # 원산지 데이터를 데이터베이스에서 가져오는 함수
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
