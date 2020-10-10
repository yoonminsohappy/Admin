import string
import random

class CouponService:
    def __init__(self, coupon_dao, config):
        self.coupon_dao = coupon_dao
        self.config     = config

    def generate_serial_numbers(self):
        serial_number = ""

        for i in range(0, 14):
            serial_number += random.choice(string.ascii_letters)
            if i == 4 or i == 9:
                serial_number += '-'
        
        return serial_number

    def make_coupon(self, conn, coupon_data):
        ISSUE_TYPE_SERIAL_NUMBER = 3 # 발급 유형 시리얼 넘버 

        if not (coupon_data['issue_id'] == ISSUE_TYPE_SERIAL_NUMBER and coupon_data['limit_count']):
            raise TypeError("COUPON_DATE_CANNOT_BE_NULL")

        coupon_id = self.coupon_dao.create_coupon(conn)
        coupon_data['coupon_id'] = coupon_id
        self.coupon_dao.create_coupon_detail(conn, coupon_data)
        
        for i in range(0, coupon_data['limit_count']):
            serial_number = self.generate_serial_numbers()
            self.coupon_dao.create_serial_number(conn, (coupon_id, serial_number,))

    def get_coupons(self, conn, params):
        # 조건에 해당하는 전체 쿠폰 카운트 가져오기
        coupon_count = self.coupon_dao.find_coupon_counts(conn, params)
        if isinstance(coupon_count, tuple):
            coupon_count = coupon_count[0]

        # limit 개수의 쿠폰만 가져오기
        coupons = self.coupon_dao.find_coupons(conn, params)

        return {"total_count": coupon_count, "coupons": coupons}