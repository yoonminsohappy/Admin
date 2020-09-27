import pymysql
from flask import jsonify
from connection import get_connection

class DAOInsertFailError(Exception):
    def __init__(self, message):
        super().__init__(message)


# 작성자: 김태수
# 수정일: 2020.09.21.월
# Product와 연결된 Class
class ProductDao:
    # 작성자: 김태수
    # 작성일: 2020.09.21.월
    # 원산지 데이터를 데이터베이스에서 가져오는 함수
    def get_country_of_origin(self, db, country_id):
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT id, name
            FROM tests
            WHERE id = %s;
            """

            cursor.execute(sql, country_id)
            result = cursor.fetchone()
        except:
            raise
        else:
            return result if result else None
        finally:
            cursor.close()

    def find_first_categories_by_seller_property_id(self, conn, seller_property_id):
        """
        1차 카테고리를 셀러 속성 아이디로 조회한다.

        Args:
            conn              : 데이터베이스 커넥션 객체
            seller_property_id: 셀러 속성 아이디

        Returns:
            results: 1차 카테고리 정보를 담은 딕셔너리 리스트
                [
                    {
                        "id"  : 1차 카테고리 아이디,
                        "name": 1차 카테고리 이름
                    },
                    ...
                ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-22(이충희): 초기 생성
            2020-09-23(이충희): 데이터베이스 커넥션 부분을 뷰 레벨로 이동시킴
        """
        QUERY = """
            SELECT
	            t2.id, t2.name 
            FROM 
	            first_category_seller_properties AS t1 
            LEFT JOIN 
	            first_categories AS t2 
            ON       
	            t1.first_category_id = t2.id 
            WHERE 
	            seller_property_id = %s;
            """
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(QUERY, (seller_property_id,))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None

    def find_second_categories_by_first_category_id(self, conn, first_category_id):
        """
        2차 카테고리를 1차 카테고리 아이디로 조회한다.

        Args:
            conn              : 데이터베이스 커넥션 객체
            first_category_id : 1차 카테고리 아이디

        Returns:
            results: 2차 카테고리 정보를 담은 딕셔너리 리스트
                [
                    {
                        "id"  : 2차 카테고리 아이디,
                        "name": 2차 카테고리 이름
                    },
                    ...
                ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-22(이충희): 초기 생성
            2020-09-23(이충희): 데이터베이스 커넥션 부분을 뷰 레벨로 이동시킴
        """
        sql = """
            SELECT
                t2.id, t2.name 
            FROM 
                first_category_second_categories AS t1 
            LEFT JOIN 
                second_categories AS t2 
            ON 
                t1.second_category_id = t2.id 
            WHERE 
                first_category_id = %s;
            """
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(sql, (first_category_id,))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None
        
    def find_categories_id(self, conn, first_category_id, second_category_id):
        """
        1차-2차 중간테이블 아이디 찾기

        Args:
            conn              : 데이터베이스 커넥션 객체
            first_category_id : 1차 카테고리 아이디
            second_category_id: 2차 카테고리 아이디

        Returns:
            result: 1차-2차 중간테이블 아이디

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-22(이충희): 초기 생성
            2020-09-23(이충희): 데이터베이스 커넥션 부분을 뷰 레벨로 이동시킴
        """
        sql = """
            SELECT 
                id
            FROM
                first_category_second_categories
            WHERE
                first_category_id = %s
            AND
                second_category_id = %s;
        """
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(sql, (first_category_id, second_category_id,))
        result = cursor.fetchone()

        cursor.close()

        return result if result else None

    def create_product(self, conn, product_dict):
        """
        상품을 등록한다.

        Args:
            conn        : 데이터베이스 커넥션 객체
            product_dict: 상품 딕셔너리
                {
                    "code"         : 상품 코드
                    "seller_id"    : 셀러 아이디,
                    "categories_id": 1차-2차 카테고리 중간테이블 아이디
                }

        Returns:
            result: 상품 아이디

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-27(이충희): 초기 생성
        """
        sql = """
            INSERT INTO products (
                code,
                seller_id,
                categories_id
            ) VALUES (
                %(code)s,
                %(seller_id)s,
                %(categories_id)s
            );
        """
        cursor = conn.cursor()

        rows = cursor.execute(sql, product_dict)
        if rows <= 0:
            raise pymysql.err.InternalError(10001, "DAO_COULD_NOT_INSERT_PRODUCT")

        result = cursor.lastrowid
        
        cursor.close()

        return result if result else None

    def create_product_detail(self, conn, product_detail_dict):
        """
        상품 등록시 상품 상세 정보를 생성한다.

        Args:
            conn               : 데이터베이스 커넥션 객체
            product_detail_dict: 상품 상세 정보 딕셔너리
                {
                    "name"                : 상품 이름,
                    "is_sold"             : 판매중 여부,
                    "is_displayed"        : 전시 여부,
                    "origin_company"      : 제조사(수입사),
                    "origin_date"         : 제조일자,
                    "simple_description"  : 한줄 설명,
                    "description"         : 상세 설명,
                    "sale_price"          : 판매가,
                    "discount_rate"       : 할인율,
                    "discount_started_at" : 할인 시작 날짜,
                    "discount_ended_at"   : 할인 종료 날짜,
                    "minimum_sale_amount" : 최소 판매량,
                    "maximum_sale_amount" : 최대 판매량,
                    "modifier_id"         : 수정자 아이디,
                    "product_id"          : 상품 아이디,
                    "country_of_origin_id": 원산지(국가) 아이디
                }

        Returns:
        
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-27(이충희): 초기 생성
        """
        sql = """
            INSERT INTO product_details (
                name,
                is_sold,
                is_displayed,
                origin_company,
                origin_date,
                simple_description,
                description,
                sale_price,
                discount_rate,
                discount_started_at,
                discount_ended_at,
                minimum_sale_amount,
                maximum_sale_amount,
                modifier_id,
                product_id,
                country_of_origin_id
            ) VALUES (
                %(name)s,
                %(is_sold)s,
                %(is_displayed)s,
                %(origin_company)s,
                %(origin_date)s,
                %(simple_description)s,
                %(description)s,
                %(sale_price)s,
                %(discount_rate)s,
                %(discount_started_at)s,
                %(discount_ended_at)s,
                %(minimum_sale_amount)s,
                %(maximum_sale_amount)s,
                %(modifier_id)s,
                %(product_id)s,
                %(country_of_origin_id)s
            );
        """
        cursor = conn.cursor()

        rows = cursor.execute(sql, product_detail_dict)
        if rows <= 0:
            raise pymysql.err.InternalError(10002, "DAO_COULD_NOT_INSERT_PRODUCT_DETAIL")

        cursor.close()

    def create_product_image(self, conn, url, order, product_id):
        """
        상품 등록시 이미지 정보를 생성한다.

        Args:
            conn      : 데이터베이스 커넥션 객체
            url       : S3에 업로드된 이미지 URL
            order     : 이미지가 보여지는 순서
            product_id: 상품 아이디

        Returns:
        
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-27(이충희): 초기 생성
        """
        sql = """
            INSERT INTO product_images (
                image_path,
                ordering,
                product_id
            ) VALUES (
                %s,
                %s,
                %s
            );
        """
        cursor = conn.cursor()

        rows = cursor.execute(sql, (url, order, product_id,))
        if rows <= 0:
            raise pymysql.err.InternalError(10003, "DAO_COULD_NOT_INSERT_PRODUCT_IMAGE")

        cursor.close()

    def create_option(self, conn, option):
        """
        상품 등록시 옵션 정보를 생성한다.

        Args:
            conn  : 데이터베이스 커넥션 객체
            option: 상품 옵션 정보 딕셔너리
                {
                    "stock"     : 재고량,
                    "color_id"  : 컬러 아이디,
                    "size_id"   : 사이즈 아이디,
                    "product_id": 상품 아이디,
                }

        Returns:
        
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-27(이충희): 초기 생성
        """
        sql = """
            INSERT INTO options (
                stock,
                color_id,
                size_id,
                product_id
            ) VALUES (
                %(stock)s,
                %(color_id)s,
                %(size_id)s,
                %(product_id)s
            );
        """
        cursor = conn.cursor()
        rows = cursor.execute(sql, option)
        if rows <= 0:
            raise pymysql.err.InternalError(10004, "DAO_COULD_NOT_INSERT_PRODUCT_OPTION")

        cursor.close()