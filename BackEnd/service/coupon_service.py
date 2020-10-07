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
        ISSUE_TYPE_SERIAL_NUMBER = 3

        coupon_id                = self.coupon_dao.create_coupon(conn)
        
        coupon_data['coupon_id'] = coupon_id
        self.coupon_dao.create_coupon_detail(conn, coupon_data)
        
        if coupon_data['issue_id'] == ISSUE_TYPE_SERIAL_NUMBER and coupon_data['limit_count']:
            for i in range(0, coupon_data['limit_count']):
                serial_number = self.generate_serial_numbers()
                self.coupon_dao.create_serial_number(conn, (coupon_id, serial_number,))