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
        S3에 이벤트 이미지 저장 - Business Layer(service) function
        Args:
            image    : 이미지 파일
            filename : S3에 저장될 때 파일명
        Returns :
            image_url
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
        """
        기획전 등록 - Business Layer(service) function
        Args:
            arguments = {
                'banner_image'              : 배너이미지,
                'detail_image'              : 상세이미지,
                'event_type'                : 기획전 타입,
                'event_kind'                : 기획전 종류,
                'is_exposed'                : 노출 여부,
                'name'                      : 기획전 이름,
                'simple_description'        : 간략 설명,
                'detail_description'        : 상세 설명,
                'started_at'                : 시작일자,
                'ended_at'                  : 종료일자,
                'event_button_name'         : 이벤트 버튼 이름,
                'event_button_link_type'    : 이벤트 버튼 링크 타입,
                'event_button_link_content' : 이벤트 버튼 링크 내용,
                'youtube_video_url'         : 유튜브 영상 링크,
                'button_product'            : 버튼 상품,
                'coupon_id'                 : 쿠폰 아이디
            }
            db = DATABASE Connection Instance
        Returns :
            ''
        Author :
            김태수
        History:
            2020-10-07 : 초기 생성
        """

        arguments['event_id'] = self.event_dao.post_event(db)

        # 배너이미지가 존재할 경우
        if arguments['banner_image'] is not None:
            banner_image_filename     = 'banner_' + str(arguments['event_id']) + secure_filename(arguments['banner_image'].filename)
            arguments['banner_image'] = self.save_event_picture(arguments['banner_image'], banner_image_filename)

        # 상세이미지가 존재할 경우
        if arguments['detail_image'] is not None:
            detail_image_filename     = 'detail_' + str(arguments['event_id']) + secure_filename(arguments['detail_image'].filename)
            arguments['detail_image'] = self.save_event_picture(arguments['detail_image'], detail_image_filename)

        arguments['event_type_id'] = self.event_dao.get_event_type_id(
            db,
            {'event_type':arguments['event_type']})['id']

        arguments['event_kind_id'] = self.event_dao.get_event_kind_id(
            db,
            {'event_kind'    : arguments['event_kind'],
             'event_type_id' : arguments['event_type_id']})['id']

        # 시작일자와 종료일자를 통해 등록 시 현재 기획전 상태 부여
        if datetime.fromisoformat(arguments['started_at']) > datetime.today():
            arguments['event_status'] = '대기'
        elif datetime.fromisoformat(arguments['started_at']) <= datetime.today() and datetime.fromisoformat(arguments['ended_at']) >= datetime.today():
            arguments['event_status'] = '진행중'
        else:
            arguments['event_status'] = '종료'

        arguments['event_status_id'] = self.event_dao.get_event_status_id(
            db,
            {'event_status':arguments['event_status']})['id']

        arguments['event_button_link_type_id'] = None
        # 기획전 이벤트 버튼 링크 타입이 존재할 경우
        if arguments['event_button_link_type']:
            arguments['event_button_link_type_id'] = self.event_dao.get_event_button_link_type_id(
                db,
                {'event_button_link_type':arguments['event_button_link_type']})['id']

        # 가상의 버튼인지 아닌지 여부 판단
        if len(arguments['button_product']) > 1:
            is_exist = 1
        else:
            is_exist = 0

        count = 0

        # 버튼에 따라 할당된 상품을 중간테이블에 등록
        for button in arguments['button_product']:
            button_id = self.event_dao.post_event_buttons(
                db,
                {'name'     : button['name'],
                 'order'    : button['order'],
                 'event_id' : arguments['event_id'],
                 'is_exist' : is_exist})

            for index, product_id in enumerate(button['product_ids']):
                self.event_dao.post_product_events(
                    db,
                    {'product_id' : product_id,
                     'order'      : index + 1,
                     'button_id'  : button_id})

                count += 1

        arguments['mapped_product_count'] = count

        # 후에 인자로 전달될 때 문제가 생기는 요소 삭제
        del(arguments['button_product'])

        self.event_dao.post_event_detail(db, arguments)

        return ''

    def get_event_list(self, db, arguments):
        """
        기획전 리스트 - Business Layer(service) function
        Args:
            arguments = {
                'event_name'   : 기획전 이름,
                'event_number' : 기획전 번호,
                'event_status' : 기획전 상태,
                'start_date'   : 등록일자 검색 시작일자,
                'end_date'     : 등록일자 검색 종료일자,
                'is_exposed'   : 노출여부,
                'event_type'   : 기획전 타입
            }
            db = DATABASE Connection Instance
        Returns :
            event_list = [{
                'event_number'         : 기획전 번호,
                'event_name'           : 기획전 명,
                'event_status_name'    : 기획전 상태 명,
                'event_type_name'      : 기획전 타입 명,
                'event_kind_name'      : 기획전 종류 명,
                'started_at'           : 시작일자,
                'ended_at'             : 종료일자,
                'is_exposed'           : 노출여부,
                'register_date'        : 등록일자,
                'mapped_product_count' : 매핑 상품 수,
                'view_count'           : 조회 수
            }]
        Author :
            김태수
        History:
            2020-10-07 : 초기 생성
        """

        event_list = self.event_dao.get_event_list(db, arguments)

        # 날짜 형식 맞추는 반복문
        for event in event_list:
            event['started_at']    = event['started_at'].isoformat(' ')
            event['ended_at']      = event['ended_at'].isoformat(' ')
            event['register_date'] = event['register_date'].isoformat(' ')

        return event_list

    def delete_event(self, db, arguments):
        """
        기획전 삭제 - Business Layer(service) function
        Args:
            arguments = {
                'event_id' : 기획전 아이디
            }
            db = DATABASE Connection Instance
        Returns :
            ''
        Author :
            김태수
        History:
            2020-10-07 : 초기 생성
        """
        self.event_dao.delete_event(db, arguments)

        return ''

    def put_event_status(self, db):
        """
        기획전 상태 수정 - Business Layer(service) function
        Args:
            db = DATABASE Connection Instance
        Returns :
            count : 상태 변경된 개수
        Author :
            김태수
        History:
            2020-10-07 : 초기 생성
        """
        event_statuses = self.event_dao.get_event_status(db)

        count = 0

        # 상태가 올바른 상태인지 확인하는 반복문
        for event_status in event_statuses:
            # 대기중인 상태
            if datetime.fromisoformat(str(event_status['started_at'])) > datetime.today():
                if event_status['event_status_id'] != 3:
                    self.event_dao.put_event_status(db, {'event_status_id':3, 'event_id':event_status['event_id']})
                    count += 1

            # 진행중인 상태
            elif datetime.fromisoformat(str(event_status['started_at'])) <= datetime.today() and datetime.fromisoformat(str(event_status['ended_at'])) >= datetime.today():
                if event_status['event_status_id'] != 1:
                    self.event_dao.put_event_status(db, {'event_status_id':1, 'event_id':event_status['event_id']})
                    count += 1

            # 종류인 상태
            else:
                if event_status['event_status_id'] != 2:
                    self.event_dao.put_event_status(db, {'event_status_id':2, 'event_id':event_status['event_id']})
                    count += 1

        return count
