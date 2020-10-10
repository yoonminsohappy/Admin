import pymysql

class CouponDao:
    def create_coupon(self, conn):
        sql = """
            INSERT INTO coupons
            VALUES();
        """

        with conn.cursor() as cursor:
            rows = cursor.execute(sql)
            if rows <= 0:
                raise pymysql.err.InternalError(10100, "DAO_COULD_NOT_CREATE_COUPON")
        return cursor.lastrowid

    def create_coupon_detail(self, conn, params):
        sql = """
            INSERT INTO coupon_details (
                coupon_id,
                name,
                coupon_type_id,
                is_downloadable,
                coupon_issue_id,
                coupon_code,
                description,
                download_started_at,
                download_ended_at,
                valid_started_at,
                valid_ended_at,
                discount_price,
                limit_count,
                minimum_price,
                modifier_id
            )
            VALUES (
                %(coupon_id)s,
                %(name)s,
                %(type_id)s,
                %(is_downloadable)s,
                %(issue_id)s,
                %(code)s,
                %(description)s,
                %(download_started_at)s,
                %(download_ended_at)s,
                %(valid_started_at)s,
                %(valid_ended_at)s,
                %(discount_price)s,
                %(limit_count)s,
                %(minimum_price)s,
                %(modifier_id)s
            );
        """
        with conn.cursor() as cursor:
            rows = cursor.execute(sql, params)
            if rows <= 0:
                raise pymysql.err.InternalError(10101, "DAO_COULD_NOT_CREATE_COUPON_DETAIL")

    def create_serial_number(self, conn, params):
        sql = """
            INSERT INTO coupon_serial_numbers (
                coupon_id,
                serial_number
            ) VALUES (
                %s,
                %s
            );
        """
        with conn.cursor() as cursor:
            rows = cursor.execute(sql, params)
            if rows <= 0:
                raise pymysql.err.InternalError(10101, "DAO_COULD_NOT_CREATE_COUPON_SERIAL_NUMBER")

    def find_coupon_counts(self, conn, params):
        sql = """
            SELECT count(*)
            FROM coupon_details AS cd
            INNER JOIN coupon_issues AS ci 
            ON ci.id = cd.coupon_issue_id
        """

        if params['has_condition']:
            sql += ' WHERE'
            if params['id']:
                sql += ' cd.coupon_id = %(id)s AND'

            if params['name']:
                sql += ' cd.name LIKE %(name)s AND'

            if params['valid_started_from']:
                sql += ' cd.valid_started_at >= %(valid_started_from)s AND'

            if params['valid_started_to']:
                sql += ' cd.valid_started_at <= %(valid_started_to)s AND'

            if params['valid_ended_from']:
                sql += ' cd.valid_ended_at >= %(valid_ended_from)s AND'

            if params['valid_ended_to']:
                sql += ' cd.valid_ended_at <= %(valid_ended_to)s AND'

            if params['download_started_from']:
                sql += ' cd.download_started_at >= %(download_started_from)s AND'

            if params['download_started_to']:
                sql += ' cd.download_started_at <= %(download_started_to)s AND'
                    
            if params['download_ended_from']:
                sql += ' cd.download_ended_at >= %(download_ended_from)s AND'

            if params['download_ended_to']:
                sql += ' cd.download_ended_at <= %(download_ended_to)s AND'

            if params['issue_type_id']:
                sql += ' ci.id = %(issue_type_id)s AND'

            if params['is_limited'] == 'Y':
                sql += ' cd.limit_count IS NULL AND'
                    
            elif params['is_limited'] == 'N':
                sql += ' cd.limit_count IS NOT NULL AND'

            sql = sql[:-3] # remove AND

        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            if not result:
                raise pymysql.err.InternalError(10102, "DAO_COULD_NOT_COUNT_COUPONS")
            
            return result

    def find_coupons(self, conn, params):
        sql = """
            SELECT
                cd.coupon_id,
                cd.name AS coupon_name,
                cd.discount_price,
                cd.valid_started_at,
                cd.valid_ended_at,
                cd.download_started_at,
                cd.download_ended_at,
                ci.name AS issue_name,
                cd.limit_count AS is_limited,
                cd.download_count,
                cd.use_count
            FROM coupon_details AS cd
            INNER JOIN coupon_issues AS ci 
            ON ci.id = cd.coupon_issue_id
        """

        if params['has_condition']:
            sql += ' WHERE'

            if params['id']:
                sql += ' cd.coupon_id = %(id)s AND'

            if params['name']:
                sql += ' cd.name LIKE %(name)s AND'

            if params['valid_started_from']:
                sql += ' cd.valid_started_at >= %(valid_started_from)s AND'

            if params['valid_started_to']:
                sql += ' cd.valid_started_at <= %(valid_started_to)s AND'

            if params['valid_ended_from']:
                sql += ' cd.valid_ended_at >= %(valid_ended_from)s AND'

            if params['valid_ended_to']:
                sql += ' cd.valid_ended_at <= %(valid_ended_to)s AND'

            if params['download_started_from']:
                sql += ' cd.download_started_at >= %(download_started_from)s AND'

            if params['download_started_to']:
                sql += ' cd.download_started_at <= %(download_started_to)s AND'
                    
            if params['download_ended_from']:
                sql += ' cd.download_ended_at >= %(download_ended_from)s AND'

            if params['download_ended_to']:
                sql += ' cd.download_ended_at <= %(download_ended_to)s AND'

            if params['issue_type_id']:
                sql += ' ci.id = %(issue_type_id)s AND'

            if params['is_limited'] == 'Y':
                sql += ' cd.limit_count IS NULL AND'
                    
            elif params['is_limited'] == 'N':
                sql += ' cd.limit_count IS NOT NULL AND'

            sql = sql[:-3] # remove AND

        sql += ' LIMIT %(limit)s OFFSET %(offset)s;'

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return results

    def find_serials_by_coupon_id(self, conn, coupon_id):
        sql = """
            SELECT 
                s.serial_number, 
                s.used_date 
            FROM coupon_serial_numbers AS s 
            WHERE coupon_id = %s;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (coupon_id,))
            results = cursor.fetchall()
            return results