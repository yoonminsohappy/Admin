import boto3

from datetime import date

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
        if 'banner_image' in arguments:
            banner_image_filename = secure_filename("banner_" + arguments['banner_image'].filename)
            arguments['banner_image'] = self.save_event_picture(arguments['banner_image'], banner_image_filename)

        if 'detail_image' in arguments:
            detail_image_filename = secure_filename("detail_"+ arguments['detail_image'].filename)
            arguments['detail_image'] = self.save_event_picture(arguments['detail_image'], detail_image_filename)

        arguments['event_type_id'] = self.event_dao.get_event_type_id(
            db,
            {'event_type':arguments['event_type']}
        )['id']

        if arguments['event_type_id'] == 2:
            arguments['event_kind_id'] = arguments['event_kind']

        else:
            arguments['event_kind_id'] = self.event_dao.get_event_kind_id(
                db,
                {
                    'event_kind'    : arguments['event_kind'],
                    'event_type_id' : arguments['event_type_id']
                }
            )['id']

        arguments['event_id'] = self.event_dao.post_event(db)

        if date.fromisoformat(arguments['started_at']) > date.today():
            arguments['event_status'] = '대기'
        elif date.fromisoformat(arguments['started_at']) <= date.today() and date.fromisoformat(arguments['ended_at']) >= date.today():
            arguments['event_status'] = '진행중'
        else:
            arguments['event_status'] = '종료'

        arguments['event_status_id'] = self.event_dao.get_event_status_id(db, {'event_status':arguments['event_status']})['id']


        arguments['event_button_link_type_id'] = None
        if arguments['event_button_link_type']:
            arguments['event_button_link_type_id'] = self.event_dao.get_event_button_link_type_id(
                db,
                {'event_button_link_type':arguments['event_button_link_type']}
            )

        if len(arguments['button_product']) > 1:
            is_exist = 1
        else:
            is_exist = 0

        count = 0

        for button in arguments['button_product']:
            button_id = self.event_dao.post_event_buttons(
                db,
                {
                    'name':button['name'],
                    'order':button['order'],
                    'event_id':arguments['event_id'],
                    'is_exist':is_exist
                }
            )

            for index, product_id in enumerate(button['product_ids']):
                self.event_dao.post_product_events(
                    db,
                    {
                        'product_id':product_id,
                        'order':index + 1,
                        'button_id':button_id
                    }
                )
                count += 1

        arguments['mapped_product_count'] = count
        del(arguments['button_product'])
        self.event_dao.post_event_detail(db, arguments)

        return ''
