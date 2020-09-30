import csv
import datetime
import string
import random
import uuid

class CouponService:
    def __init__(self, coupon_dao, config):
        self.coupon_dao = coupon_dao
        self.config     = config

    def generate_serial_numbers(self):
        """
        시리얼 넘버 생성

        Args:

        Returns:
            serial_number: 시리얼 넘버

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        serial_number = ""

        for i in range(0, 14):
            serial_number += random.choice(string.ascii_letters)
            if i == 4 or i == 9:
                serial_number += '-'
        
        return serial_number

    def make_coupon(self, conn, coupon_data):
        """
        쿠폰 생성

        Args:
            conn       : 데이터베이스 커넥션 객체
            coupon_data: 쿠폰 정보 딕셔너리

        Returns:
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        ISSUE_TYPE_SERIAL_NUMBER = 3 # 발급 유형 시리얼 넘버     

        coupon_id = self.coupon_dao.create_coupon(conn)
        coupon_data['coupon_id'] = coupon_id
        self.coupon_dao.create_coupon_detail(conn, coupon_data)
        
        if coupon_data['issue_id'] == ISSUE_TYPE_SERIAL_NUMBER:
            if not coupon_data['limit_count']:
                raise TypeError("COUPON_LIMIT_COUNT_CANNOT_BE_NULL")
            
            for i in range(0, coupon_data['limit_count']):
                serial_number = self.generate_serial_numbers()
                self.coupon_dao.create_serial_number(conn, (coupon_id, serial_number,))

    def get_coupons(self, conn, params):
        """
        쿠폰 리스트 조회

        Args:
            conn  : 데이터베이스 커넥션 객체
            params: 쿠폰 정보 딕셔너리

        Returns:
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        # 조건에 해당하는 전체 쿠폰 카운트 가져오기
        coupon_count = self.coupon_dao.find_coupon_counts(conn, params)
        if isinstance(coupon_count, tuple):
            coupon_count = coupon_count[0]

        if coupon_count != None and coupon_count > 0:
            # limit 개수의 쿠폰만 가져오기
            coupons = self.coupon_dao.find_coupons(conn, params)
            print(coupons)
        else:
            coupon_count = 0
            coupons = []

        return {"total_count": coupon_count, "coupons": coupons}

    def make_serials_csv(self, serials):
        """
        시리얼 넘버 csv 파일 만들기

        Args:
            serials: 시리얼 넘버 리스트

        Returns:
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        tmp_filename = f'temp/{str(uuid.uuid4())}.csv'
        with open(tmp_filename, 'w', encoding='utf-8') as f:
            wr = csv.writer(f)
            wr.writerow(['번호', '시리얼번호', '사용일시']) # 헤더

            # 로우
            for idx, row in enumerate(serials):
                wr.writerow([idx+1, row['serial_number'], row['used_date'] if row['used_date'] else '-'])
        
        return tmp_filename

    def make_download_filename(self, coupon_id):
        """
        유저에게 보여질 다운로드 파일 이름 만들기

        Args:
            coupon_id: 쿠폰 아이디

        Returns:
            다운로드할 파일 경로 + 파일명

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        now_date = datetime.datetime.now().strftime("%Y%m%d")
        return f'{now_date}_{coupon_id}_SERIAL_NUMBER.csv'
        
    def download_serials(self, conn, coupon_id):
        """
        시리얼 넘버 csv 파일을 만든다.

        Args:
            conn     : 데이터베이스 커넥션 객체
            coupon_id: 쿠폰 아이디

        Returns:
            실제 서버에 위치한 파일 경로+이름,
            유저에게 보여지는 파일 이름

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        serials = self.coupon_dao.find_serials_by_coupon_id(conn, coupon_id)
        if not serials:
            raise TypeError(f'NO_SERIALS_FOR_COUPON_{coupon_id}')

        tmp_filename      = self.make_serials_csv(serials)
        download_filename = self.make_download_filename(coupon_id)
        return tmp_filename, download_filename

    def remove_coupon(self, conn, coupon_id):
        """
        쿠폰 제거

        Args:
            conn     : 데이터베이스 커넥션 객체
            coupon_id: 쿠폰 아이디

        Returns:

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        self.coupon_dao.delete_coupon_is_deleted(conn, coupon_id)

    def get_coupon_code(self, conn, coupon_id):
        """
        쿠폰 코드 조회

        Args:
            conn     : 데이터베이스 커넥션 객체
            coupon_id: 쿠폰 아이디

        Returns:
        
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        result = self.coupon_dao.find_coupon_code_by_id(conn, coupon_id)
        if not result:
            raise TypeError(f'NO_COUPON_CODE_FOR_COUPON_{coupon_id}')
            # raise TypeError({'errorCode': 'NO_COUPON_CODE_FOR_COUPON', 'coupon_id': coupon_id})
        return result

    def get_coupon_info(self, conn, coupon_id):
        """
        쿠폰 상세 정보 조회

        Args:
            conn     : 데이터베이스 커넥션 객체
            coupon_id: 쿠폰 아이디

        Returns:
        
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        result = self.coupon_dao.find_coupon_by_id(conn, coupon_id)
        if not result:
            raise TypeError(f'NO_COUPON_INFO_FOR_COUPON_{coupon_id}')
        return result

    def update_coupon_info(self, conn, params):
        """
        쿠폰 수정

        Args:
            conn     : 데이터베이스 커넥션 객체
            coupon_id: 쿠폰 아이디

        Returns:
        
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        self.coupon_dao.update_coupon_detail(conn, params)