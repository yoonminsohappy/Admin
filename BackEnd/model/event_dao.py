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
            youtube_video_url
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
            %(youtube_video_url)s
            )

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
