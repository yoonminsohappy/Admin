import pymysql

from pymysql import err

class EventDao:
    def post_event(self, db):
        sql = """
        INSERT INTO events
            (is_deleted)
        VALUES
            (0);
        """
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.lastrowid

            if not result:
                raise err.OperationalError

            return result

        raise err.OperationalError

    def post_event_detail(self, db, arguments):
        """
        주문정보 - Persistence Layer(model) function
        Args:
            arguments = {
            }
            db = DATABASE Connection Instance
        Returns :
        Author :
            김태수
        History:
            2020-10-07 : 초기 생성
        """

        sql = """
        INSERT INTO event_details
            (
            event_id,
            name,
            event_status_id,
            event_type_id,
            register_date,
            started_at,
            ended_at,
            is_event_exposed,
            banner_image_url,
            detail_image_url,
            modifier_id,
            created_at,
            expired_at,
            mapped_product_count,
            view_count,
            event_button_name,
            event_button_link_type_id,
            event_button_link_content,
            event_simple_description,
            event_detail_description,
            youtube_video_url,
            event_kind_id,
            coupon_id
            )
        VALUES
            (
            %(event_id)s,
            %(name)s,
            %(event_status_id)s,
            %(event_type_id)s,
            NOW(),
            %(started_at)s,
            %(ended_at)s,
            %(is_exposed)s,
            %(banner_image)s,
            %(detail_image)s,
            null,
            NOW(),
            '9999-12-31',
            %(mapped_product_count)s,
            0,
            %(event_button_name)s,
            %(event_button_link_type_id)s,
            %(event_button_link_content)s,
            %(simple_description)s,
            %(detail_description)s,
            %(youtube_video_url)s,
            %(event_kind_id)s,
            %(coupon_id)s
            );
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, arguments)

            if not result:
                raise ValueError

            return result

        raise err.OperationalError

    def get_event_type_id(self, db, arguments):
        """
        이벤트 타입 아이디 - Persistence Layer(model) function
        Args:
            arguments = {
                "event_type" : 이벤트 타입 이름
            }
        Returns:
            ValueError
            event_type_id = {
                'id' : 이벤트 타입 아이디
            }
        Author:
            김태수
        History:
            2020-10-07 : 초기 생성
        """

        sql = """
        SELECT
            id
        FROM
            event_types
        WHERE
            name = %(event_type)s;
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            event_type_id = cursor.fetchone()

            if not event_type_id:
                raise ValueError

            return event_type_id

        raise err.OperationalError

    def get_event_kind_id(self, db, arguments):
        """
        이벤트 종류 아이디 - Persistence Layer(model) function
        Args:
            arguments = {
                "event_kind"    : 이벤트 종류 이름
                "event_type_id" : 이벤트 타입 아이디
            }
        Returns:
            ValueError
            event_kind_id = {
                'id' : 이벤트 종류 아이디
            }
        Author:
            김태수
        History:
            2020-10-07 : 초기 생성
        """
        sql = """
        SELECT
            id
        FROM
            event_kinds
        WHERE
            name = %(event_kind)s
            AND event_type_id = %(event_type_id)s;
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            event_kind_id = cursor.fetchone()

            if not event_kind_id:
                raise ValueError

            return event_kind_id

        raise err.OperationalError

    def get_event_status_id(self, db, arguments):
        sql = """
        SELECT
            id
        FROM
            event_statuses
        WHERE
            name = %(event_status)s;
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            event_status_id = cursor.fetchone()

            if not event_status_id:
                raise ValueError

            return event_status_id

        raise err.OperationalError

    def get_event_button_link_type_id(self, db, arguments):
        sql = """
        SELECT
            id
        FROM
            event_button_link_types
        WHERE
            name = %(event_button_link_type)s;
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            event_button_link_type_id = cursor.fetchone()

            if not event_button_link_type_id:
                raise ValueError

            return event_button_link_type_id

        raise err.OperationalError

    def post_event_buttons(self, db, arguments):
        sql = """
        INSERT INTO event_buttons
        (
        `name`,
        `order`,
        `event_id`,
        `is_exist`
        )
        VALUES
        (
        %(name)s,
        %(order)s,
        %(event_id)s,
        %(is_exist)s
        );
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            result = cursor.lastrowid

            if not result:
                raise err.OperationalError

            return result

        raise err.OperationalError

    def post_product_events(self, db, arguments):
        sql = """
        INSERT INTO product_events
        (
        `product_id`,
        `order`,
        `button_id`
        )
        VALUES
        (
        %(product_id)s,
        %(order)s,
        %(button_id)s
        );
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, arguments)

            if not result:
                raise err.OperationalError

            return result

        raise err.OperationalError

    def get_event_list(self, db, arguments):
        sql_1 = """
        SELECT
            e.id AS event_number,
            ed.name AS event_name,
            es.name AS event_status_name,
            et.name AS event_type_name,
            ek.name AS event_kind_name,
            ed.started_at AS started_at,
            ed.ended_at AS ended_at,
            ed.is_event_exposed AS is_exposed,
            ed.register_date AS register_date,
            ed.mapped_product_count AS mapped_product_count,
            ed.view_count AS view_count
        FROM
            events e
        LEFT JOIN
            event_details ed
            ON e.id = ed.event_id
        LEFT JOIN
            event_statuses es
            ON ed.event_status_id = es.id
        LEFT JOIN
            event_types et
            ON et.id = ed.event_type_id
        LEFT JOIN
            event_kinds ek
            ON ek.id = ed.event_kind_id
        WHERE
            e.is_deleted = 0
            AND ed.expired_at = '9999-12-31'
        """

        sql_2 = """
        ORDER BY
            e.id DESC;
        """

        if arguments['event_name'] != "%\%":
            sql_1 += " AND ed.name LIKE %(event_name)s"
        if arguments['event_number']:
            sql_1 += " AND e.id = %(event_number)s"
        if arguments['event_status']:
            sql_1 += " AND ed.event_status_id = %(event_status)s"
        if arguments['start_date'] and arguments['end_date']:
            sql_1 += " AND ed.register_date >= %(start_date)s AND ed.register_date <= %(end_date)s"
        if arguments['is_exposed']:
            sql_1 += " AND ed.is_event_exposed = %(is_exposed)s"
        if arguments['event_type']:
            sql_1 += " AND ed.event_type_id IN %(event_type)s"

        sql = sql_1 + sql_2

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            event_list = cursor.fetchall()

            return event_list

        raise err.OperationalError

    def delete_event(self, db, arguments):
        sql = """
        UPDATE
            events
        SET
            is_deleted = '1'
        WHERE
            id = %(event_id)s;
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, arguments)

            if not result:
                raise err.OperationalError

            return ''

        raise err.OperationalError

    def get_event_status(self, db):
        sql = """
        SELECT
            e.id AS event_id,
            es.id AS event_status_id,
            ed.started_at AS started_at,
            ed.ended_at AS ended_at
        FROM
            events e
        LEFT JOIN
            event_details ed
            ON e.id = ed.event_id
        LEFT JOIN
            event_statuses es
            ON ed.event_status_id = es.id
        LEFT JOIN
            event_types et
            ON et.id = ed.event_type_id
        LEFT JOIN
            event_kinds ek
            ON ek.id = ed.event_kind_id
        WHERE
            e.is_deleted = 0
            AND es.id IN (1, 3)
            AND ed.expired_at = '9999-12-31'
        ORDER BY
            e.id DESC;
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

            return result

        raise err.OperationalError

    def put_event_status(self, db):
        sql = """
        UPDATE
            event_details
        SET
            event_status_id = %(event_status_id)s
        WHERE
            id = %(event_id)s
            AND expired_at = '9999-12-31';
        """

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql)

            if not result:
                raise err.OperationalError

            return ''

        raise err.OperationalError
