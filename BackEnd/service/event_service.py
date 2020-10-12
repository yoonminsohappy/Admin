import boto3

from datetime import datetime

from werkzeug.utils import secure_filename

class EventService:
    def __init__(self, event_dao, config):
        self.event_dao = event_dao
        self.config = config
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id     = config['S3_ACCESS_KEY_EVENT'],
            aws_secret_access_key = config['S3_SECRET_KEY_EVENT']
        )

    def save_event_picture(self, image, filename):
        """
        이벤트 이미지 저장 - Business Layer(service) function
        Args:
            arguments = {
            }
            db = DATABASE Connection Instance
        Returns :
            }]
        Author :
            김태수
        History:
            2020-10-07 : 초기 생성
        """
        self.s3.upload_fileobj(
            image,
            self.config['S3_BUCKET_EVENT'],
            filename
        )

        return f"{self.config['S3_BUCKET_URL_EVENT']}{filename}"

    def post_event(self, db, arguments):
        if arguments['banner_image'] is not None:
            banner_image_filename     = 'banner_' + secure_filename(arguments['banner_image'].filename)
            arguments['banner_image'] = self.save_event_picture(arguments['banner_image'], banner_image_filename)

        if arguments['detail_image'] is not None:
            detail_image_filename     = 'detail_' + secure_filename(arguments['detail_image'].filename)
            arguments['detail_image'] = self.save_event_picture(arguments['detail_image'], detail_image_filename)

        arguments['event_type_id'] = self.event_dao.get_event_type_id(
            db,
            {'event_type':arguments['event_type']})['id']

        arguments['event_kind_id'] = self.event_dao.get_event_kind_id(
            db,
            {'event_kind'    : arguments['event_kind'],
             'event_type_id' : arguments['event_type_id']})['id']

        arguments['event_id'] = self.event_dao.post_event(db)

        if datetime.fromisoformat(arguments['started_at']) > datetime.today():
            arguments['event_status'] = '대기'
        elif datetime.fromisoformat(arguments['started_at']) <= datetime.today() and datetime.fromisoformat(arguments['ended_at']) >= datetime.today():
            arguments['event_status'] = '진행중'
        else:
            arguments['event_status'] = '종료'

        arguments['event_status_id'] = self.event_dao.get_event_status_id(db, {'event_status':arguments['event_status']})['id']

        arguments['event_button_link_type_id'] = None
        if arguments['event_button_link_type']:
            arguments['event_button_link_type_id'] = self.event_dao.get_event_button_link_type_id(
                db,
                {'event_button_link_type':arguments['event_button_link_type']})['id']

        if len(arguments['button_product']) > 1:
            is_exist = 1
        else:
            is_exist = 0

        count = 0

        for button in arguments['button_product']:
            button_id = self.event_dao.post_event_buttons(
                db,
                {'name':button['name'],
                 'order':button['order'],
                 'event_id':arguments['event_id'],
                 'is_exist':is_exist})

            for index, product_id in enumerate(button['product_ids']):
                self.event_dao.post_product_events(
                    db,
                    {'product_id':product_id,
                     'order':index + 1,
                     'button_id':button_id})
                count += 1

        arguments['mapped_product_count'] = count
        del(arguments['button_product'])
        self.event_dao.post_event_detail(db, arguments)

        return ''

    def get_event_list(self, db, arguments):
        event_list = self.event_dao.get_event_list(db, arguments)

        for event in event_list:
            event['started_at']    = event['started_at'].isoformat()
            event['ended_at']      = event['ended_at'].isoformat()
            event['register_date'] = event['register_date'].isoformat()

        return event_list
