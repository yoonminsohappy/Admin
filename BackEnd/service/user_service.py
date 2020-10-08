import json, bcrypt, jwt
from flask_paginate import Pagination, get_page_args

#유저 검색, 전체리스트
class UserService:
    def __init__(self, dao, config):
        self.dao = dao
        self.config = config

    def search_user_list(self, conn, search_info):
        results = {}

        if search_info is None:
            raise Exception("INVALID_PARAMETER")

        total_count = self.dao.find_search_total_user_list(conn, search_info)

        total_page  = int(total_count/10)+1

        user_list = []

        if search_info['page'] <= total_page:
            user_list = self.dao.find_search_user_list(conn, search_info)
            
        results['user_list']    = user_list
        results['total_page']   = int(total_count/10)+1
        results['total_count']  = total_count
        
        return results