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
        sql = """
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
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (seller_property_id,))
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10007, "DAO_COULD_NOT_SELECT_FIRST_CATEGRORIES")

        return results

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
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (first_category_id,))
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10006, "DAO_COULD_NOT_SELECT_SECOND_CATEGRORIES")

        return results
        
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
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (first_category_id, second_category_id,))
            result = cursor.fetchone()
            if not result:
                raise pymysql.err.InternalError(10005, "DAO_COULD_NOT_SELECT_CATEGORIES")

        return result

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
        with conn.cursor() as cursor:
            rows = cursor.execute(sql, product_dict)
            result = cursor.lastrowid
            if rows <= 0 or not result:
                raise pymysql.err.InternalError(10001, "DAO_COULD_NOT_INSERT_PRODUCT")

        return result

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
        with conn.cursor() as cursor:
            rows = cursor.execute(sql, product_detail_dict)
            if rows <= 0:
                raise pymysql.err.InternalError(10002, "DAO_COULD_NOT_INSERT_PRODUCT_DETAIL")

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
        with conn.cursor() as cursor:
            rows = cursor.execute(sql, (url, order, product_id,))
            if rows <= 0:
                raise pymysql.err.InternalError(10003, "DAO_COULD_NOT_INSERT_PRODUCT_IMAGE")

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
        with conn.cursor() as cursor:
            rows = cursor.execute(sql, option)
            if rows <= 0:
                raise pymysql.err.InternalError(10004, "DAO_COULD_NOT_INSERT_PRODUCT_OPTION")

    def find_products(self, conn, params):
        sql = """
            SELECT
                p.id,
                DATE_FORMAT(CONVERT_TZ(p.register_date, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS register_date,
                pi.image_path, 
                pd.name AS product_name, 
                p.code, 
                sp.name AS seller_name, 
                si.korean_name,
                pd.sale_price,
                pd.discount_rate,
                pd.is_sold,
                pd.is_displayed
            FROM 
                product_details AS pd
            INNER JOIN products AS p 
                ON pd.product_id = p.id
            INNER JOIN product_images AS pi 
                ON pi.product_id = p.id
            INNER JOIN sellers AS s 
                ON s.id = p.seller_id
            INNER JOIN seller_informations AS si 
                ON s.id = si.seller_id
            INNER JOIN seller_properties AS sp 
                ON sp.id = si.seller_property_id
            WHERE 
                pd.expired_at = '9999-12-31 23:59:59'
            AND 
	            p.is_deleted = 0
            AND
	            s.is_deleted = 0
            AND
                si.expired_at = '9999-12-31 23:59:59'
            AND
                pi.ordering = 1
            AND 
                (
                    pd.discount_ended_at IS NULL 
                    OR
                    (
                        NOW() BETWEEN pd.discount_started_at AND pd.discount_ended_at
                    )
                )
        """
        sql2 = """
            ORDER BY
                p.register_date DESC
            LIMIT
                %(limit)s
            OFFSET
                %(offset)s;
        """
        if params['start_date'] and params['end_date']:
            sql += """
                AND
                    p.register_date BETWEEN %(start_date)s AND %(end_date)s
            """

        if params['seller_name']:
            sql += """
                AND 
                    si.korean_name LIKE %(seller_name)s
            """

        if params['product_name']:
            sql += """
                AND
                    pd.name LIKE %(product_name)s
            """

        if params['product_id']:
            sql += """
                AND
                    p.id = %(product_id)s
            """

        if params['product_code']:
            sql += """
                AND
                    p.code = %(product_code)s
            """

        if params['seller_property_ids_length'] > 0:
            sql += """
                AND (
            """
            length = params['seller_property_ids_length']
            for idx in range(0, length):
                if idx == 0 and params[f'seller_property_id_{idx}']:
                    sql += f" sp.id = %(seller_property_id_{idx})s "
                if params[f'seller_property_id_{idx}']:
                    sql += f" OR sp.id = %(seller_property_id_{idx})s "
            sql += """
                )
            """

        if params['is_sold']:
            sql += """
                AND
                    pd.is_sold = %(is_sold)s
            """

        if params['is_displayed']:
            sql += """
                AND
                    pd.is_displayed = %(is_displayed)s
            """

        if params['is_discounted']:
            sql += """
                AND
                    pd.discount_rate > 0
            """

        sql += sql2

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10008, "DAO_COULD_NOT_LIST_PRODUCTS")
        return results

    def find_product_by_code(self, conn, code):
        sql = """
            SELECT 
                p.id AS product_id,
                p.code,
                p.categories_id,
                fc.id AS first_category_id,
                fc.name,
                sc.id AS second_category_id,
                sc.name,
                pd.id AS product_detail_id,
                pd.name,
                pd.is_sold,
                pd.is_displayed,
                pd.origin_company,
                pd.origin_date,
                pd.simple_description,
                pd.description,
                pd.sale_price,
                pd.discount_rate,
                DATE_FORMAT(CONVERT_TZ(pd.discount_started_at, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS discount_started_at,
                DATE_FORMAT(CONVERT_TZ(pd.discount_ended_at, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS discount_ended_at,
                pd.minimum_sale_amount,
                pd.maximum_sale_amount,
                pd.country_of_origin_id
            FROM
                products AS p
            INNER JOIN
                product_details AS pd ON pd.product_id = p.id
            INNER JOIN
                first_category_second_categories AS fcsc ON p.categories_id = fcsc.id
            INNER JOIN
                first_categories AS fc ON fcsc.first_category_id = fc.id
            INNER JOIN
                second_categories AS sc ON fcsc.second_category_id = sc.id
            WHERE
                p.code = %s
            AND
                p.is_deleted = 0
            AND
                pd.expired_at = '9999-12-31 23:59:59';
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (code,))
            result = cursor.fetchone()
            if not result or not result['product_id']:
                raise pymysql.err.InternalError(10009, "DAO_COULD_NOT_FIND_PRODUCT")
        return result

    def find_product_images(self, conn, product_id):
        sql = """
            SELECT
                pi.id, pi.image_path, pi.ordering
            FROM
                product_images AS pi
            WHERE
                pi.product_id = %s ;
        """ 

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (product_id,))
            result = cursor.fetchall()
            if not result:
                raise pymysql.err.InternalError(10010, "DAO_COULD_NOT_FIND_PRODUCT_IMAGES")
        return result

    def find_product_options(self, conn, product_id):
        sql = """
            SELECT 
                *
            FROM
                options AS o
            INNER JOIN
                colors AS c ON o.color_id = c.id
            INNER JOIN
                sizes AS s ON o.size_id = s.id
            WHERE
                product_id = %s;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (product_id,))
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10011, "DAO_COULD_NOT_FIND_PRODUCT_OPTIONS")
        return results
    
    def find_all_countries(self, conn):
        sql = """
            SELECT 
                *
            FROM
                country_of_origins;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10011, "DAO_COULD_NOT_FIND_COUNTRIES")
        return results

    def find_all_colors(self, conn):
        sql = """
            SELECT 
                *
            FROM
                colors;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10011, "DAO_COULD_NOT_FIND_COLORS")
        return results

    def find_all_sizes(self, conn):
        sql = """
            SELECT 
                *
            FROM
                sizes;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10012, "DAO_COULD_NOT_FIND_SIZES")
        return results

    def find_products_by_dates(self, conn, start_date, end_date):
        sql = """
            SELECT 
                DATE_FORMAT(CONVERT_TZ(p.register_date, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS register_date,
                pi.image_path,
                pd.name AS product_name,
                p.code,
                p.id,
                sp.name AS seller_property_name,
                si.korean_name AS seller_name,
                pd.sale_price,
                pd.sale_price - (pd.discount_rate * 0.01 * pd.sale_price) AS discounted_price,
                pd.is_sold,
                pd.is_displayed,
                pd.discount_rate
            FROM
                products AS p
            INNER JOIN
                product_details AS pd ON p.id = pd.product_id
            INNER JOIN
                product_images AS pi ON p.id = pi.product_id
            INNER JOIN
                sellers AS s ON p.seller_id = s.id
            INNER JOIN
                seller_informations AS si ON s.id = si.seller_id
            INNER JOIN
                seller_properties AS sp ON si.seller_property_id = sp.id
            WHERE
                p.register_date BETWEEN %s AND %s
            AND
                p.is_deleted = 0
            AND
                si.expired_at = '9999-12-31 23:59:59'
            AND
                s.is_deleted = 0
            AND
                pd.expired_at = '9999-12-31 23:59:59'
            AND
                pi.ordering = 1
            ORDER BY
                p.register_date
            DESC;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (start_date, end_date,))
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10008, "DAO_COULD_NOT_LIST_PRODUCTS")
        return results

    def find_products_by_ids(self, conn, product_ids):
        sql = """
            SELECT 
                DATE_FORMAT(CONVERT_TZ(p.register_date, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS register_date,
                pi.image_path,
                pd.name AS product_name,
                p.code,
                p.id,
                sp.name AS seller_property_name,
                si.korean_name AS seller_name,
                pd.sale_price,
                pd.sale_price - (pd.discount_rate * 0.01 * pd.sale_price) AS discounted_price,
                pd.is_sold,
                pd.is_displayed,
                pd.discount_rate
            FROM
                products AS p
            INNER JOIN
                product_details AS pd ON p.id = pd.product_id
            INNER JOIN
                product_images AS pi ON p.id = pi.product_id
            INNER JOIN
                sellers AS s ON p.seller_id = s.id
            INNER JOIN
                seller_informations AS si ON s.id = si.seller_id
            INNER JOIN
                seller_properties AS sp ON si.seller_property_id = sp.id
            WHERE
                p.is_deleted = 0
            AND
                si.expired_at = '9999-12-31 23:59:59'
            AND
                s.is_deleted = 0
            AND
                pd.expired_at = '9999-12-31 23:59:59'
            AND
                pi.ordering = 1
            AND (
        """
        for idx, _id in enumerate(product_ids):
            if idx == 0:
                sql += """
                    p.id = %s
                """
            else:
                sql += """
                    OR
                        p.id = %s
                """
        sql += """)
            ORDER BY
                p.register_date
            DESC;
        """

        # raise pymysql.err.InternalError(10008, "DAO_COULD_NOT_LIST_PRODUCTS")
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, product_ids)
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10008, "DAO_COULD_NOT_LIST_PRODUCTS")
        return results

    def update_product(self, conn, product):
        sql = """
            UPDATE 
                products
            SET 
                categories_id = %(categories_id)s
            WHERE 
                id = %(product_id)s
            AND
                is_deleted = 0;
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, product)

    def find_product_detail_by_id(self, conn, product_id):
        sql = """
            SELECT  
                is_sold,
                is_displayed,
                origin_company,
                origin_date,
                country_of_origin_id,
                name,
                simple_description,
                description,
                sale_price,
                discount_rate,
                DATE_FORMAT(CONVERT_TZ(discount_started_at, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS discount_started_at,
                DATE_FORMAT(CONVERT_TZ(discount_ended_at, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS discount_ended_at,
                minimum_sale_amount,
                maximum_sale_amount
            FROM
                product_details
            WHERE
                product_id = %s
            AND
                expired_at = '9999-12-31 23:59:59'
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (product_id,))
            result = cursor.fetchone()
            if not result:
                raise pymysql.err.InternalError(10014, "DAO_COULD_NOT_FIND_PRODUCT")
        return result

    def update_product_detail(self, conn, product_detail):
        sql = """
            UPDATE
                product_details
            SET
                expired_at = NOW()
            WHERE
                product_id = %(product_id)s
            AND
                expired_at = '9999-12-31 23:59:59';
        """

        with conn.cursor() as cursor:
            rows = cursor.execute(sql, product_detail)
            if rows <= 0:
                raise pymysql.err.InternalError(10015, "DAO_COULD_NOT_UPDATE_PRODUCT_DETAIL")

        sql2 = """
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
                DATE_FORMAT(CONVERT_TZ(discount_started_at, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS discount_started_at,
                DATE_FORMAT(CONVERT_TZ(discount_ended_at, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') AS discount_ended_at,
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

        with conn.cursor() as cursor:
            rows = cursor.execute(sql2, product_detail)
            if rows <= 0:
                raise pymysql.err.InternalError(10002, "DAO_COULD_NOT_INSERT_PRODUCT_DETAIL")

    def update_option(self, conn, option):
        sql = """
            UPDATE
                options
            SET
                color_id = %(color_id)s,
                size_id = %(size_id)s,
                stock = %(stock)s
            WHERE
                product_id = %(product_id)s;
        """

        with conn.cursor() as cursor:
            rows = cursor.execute(sql, option)
            if rows <= 0:
                raise pymysql.err.InternalError(10016, "DAO_COULD_NOT_UPDATE_OPTION")

    def find_product_image(self, conn, product_id, ordering):
        sql = """
            SELECT
                *
            FROM
                product_images
            WHERE
                product_id = %s
            AND
                ordering = %s
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (product_id, ordering,))
            result = cursor.fetchone()
            return result if result else None

    def delete_product_image(self, conn, product_id, ordering):
        sql = """
            DELETE FROM
                product_images
            WHERE
                product_id = %s
            AND
                ordering = %s
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (product_id, ordering,))

    def find_product_history(self, conn, product_id):
        sql = """
            SELECT
                pd.created_at,
                pd.is_sold,
                pd.is_displayed,
                pd.sale_price,
                pd.sale_price - (pd.sale_price * 0.01 * pd.discount_rate) AS discounted_price,
                pd.discount_rate,
                si.korean_name
            FROM
                products AS p
            INNER JOIN
                product_details AS pd ON pd.product_id = p.id
            INNER JOIN
                sellers AS s ON pd.modifier_id = s.id
            INNER JOIN
                seller_informations AS si ON si.seller_id = s.id
            WHERE
                p.id = %s
            ORDER BY
                pd.created_at
            DESC;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (product_id,))
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError(10017, "DAO_COULD_NOT_FIND_PRODUCT_HISTORY")

        return results