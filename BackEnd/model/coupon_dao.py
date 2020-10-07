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
                is_limited_coupon,
                limit_count,
                is_limited_minimum_price,
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
                %(is_limited_coupon)s,
                %(limit_count)s,
                %(is_limited_minimum_price)s,
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