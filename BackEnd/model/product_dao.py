import pymysql
from flask import jsonify
from connection import get_connection

# 작성자: 김태수
# 수정일: 2020.09.21.월
# Product와 연결된 Class
class ProductDao:
    def __init__(self, db):
        self.database = get_connection(db)
        self.cursor   = self.database.cursor(pymysql.cursors.DictCursor)

    # 작성자: 김태수
    # 작성일: 2020.09.21.월
    # 원산지 데이터를 데이터베이스에서 가져오는 함수
    def get_country_of_origin(self, country_id):
        try:
            sql = """
            SELECT id, name
            FROM tests
            WHERE id = %s;
            """

            self.cursor.execute(sql, country_id)
            result = self.cursor.fetchone()
        except:
            self.database.rollback()
            self.cursor.close()
            self.database.close()
            raise
        else:
            self.database.commit()
            self.cursor.close()
            self.database.close()
            return result if result else None
