import json, bcrypt, jwt
from flask_paginate import Pagination, get_page_args

#유저 검색, 전체리스트
class UserService:
    def __init__(self, dao, config):
        self.dao = dao
        self.config = config

    def search_user_list(self, conn, search_info):
        """
        유저커뮤니티 전체리스트 , 검색 기능 API

        Args:
            conn        :   데이터베이스 커넥션 객체
            search_info :   검색 데이터를 담을 리스트

        Retruns:
            200, results : 해당 검색에 대한 결과
            400, {'message': 'UNSUCCESS'} : 검색실패시

        Authors:
            wldus9503@gmail.com(이지연)
        
        History:(
            2020.10.01(이지연)  : 초기생성
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경, register_date 날짜 형식 변경

        """
        results = {}

        if search_info is None:
            raise Exception("INVALID_PARAMETER")
        
        total_count = self.dao.find_search_total_user_list(conn, search_info)
        total_page  = int(total_count/10)+1

        user_list = []
        if search_info['page'] <= total_page:
            user_list = self.dao.find_search_user_list(conn, search_info)

        results['user_list']    = user_list
        results['total_page']   = total_page
        results['total_count']  = total_count
        
        return results