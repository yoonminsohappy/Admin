import pymysql

# 작성자: 김태수
# 수정일: 2020.09.21.월
# Product와 연결된 Class
class ProductDao:
    def __init__(self, database):
        self.db     = database
        self.cursor = self.db.cursor()

    # 작성자: 김태수
    # 작성일: 2020.09.21.월
    # 원산지 데이터를 데이터베이스에서 가져오는 함수
    def get_country_of_origin(self, country_id):
        row = self.cursor.execute(
            f"""
            SELECT
                id,
                name
            FROM country_of_origins
            WHERE id = {country_id}
            """)
        self.db.commit()

        return row if row else None
