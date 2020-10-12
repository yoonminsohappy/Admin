import json

from flask import jsonify, request
from flask.views import MethodView

from werkzeug.utils import secure_filename

import config, connection, ast

import traceback

class EventView(MethodView):
    def __init__(self, service):
        self.service = service

    def post(self):
        """
        이벤트 등록 - Presentation Layer(view) function
        Args:
            arguments = {
            }
        Returns :
            }], 200
        Author :
            김태수
        History:
            2020-10-07 : 초기 생성
        """

        try:
            db = connection.get_connection()
            data = json.loads(request.form.get('body', None))
            banner_image = request.files.get('banner_image', None)
            detail_image = request.files.get('detail_image', None)

            if 'simple_description' not in data:
                data['simple_description'] = None

            if 'detail_description' not in data:
                data['detail_description'] = None

            if 'event_button_name' not in data:
                data['event_button_name'] = None

            if 'event_button_link_type' not in data:
                data['event_button_link_type'] = None

            if 'event_button_link_content' not in data:
                data['event_button_link_content'] = None

            if 'youtube_vidoe_url' not in data:
                data['youtube_video_url'] = None

            if 'coupon_id' not in data:
                data['coupon_id'] = None

            if 'button_product' not in data:
                data['button_product'] = []
            else:
                data['button_product'] = list(data['button_product'])

            arguments = {
                'banner_image'              : banner_image,
                'detail_image'              : detail_image,
                'event_type'                : data['event_type'],
                'event_kind'                : data['event_kind'],
                'is_exposed'                : data['is_exposed'],
                'name'                      : data['name'],
                'simple_description'        : data['simple_description'],
                'detail_description'        : data['detail_description'],
                'started_at'                : data['started_at'],
                'ended_at'                  : data['ended_at'],
                'event_button_name'         : data['event_button_name'],
                'event_button_link_type'    : data['event_button_link_type'],
                'event_button_link_content' : data['event_button_link_content'],
                'youtube_video_url'         : data['youtube_video_url'],
                'button_product'            : data['button_product'],
                'coupon_id'                 : data['coupon_id']
            }

            self.service.post_event(db, arguments)

        except  KeyError:
            traceback.print_exc()
            db.rollback()
            return jsonify({'message':'KEY_ERROR'}), 400

        except:
            traceback.print_exc()
            db.rollback()
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            db.commit()
            return jsonify({'message':'SUCCESS'}), 200

        finally:
            db.close()

    def get(self):
        try:
            db = connection.get_connection()

            arguments = {
                'event_name'   : '%' + request.args.get('event_name', '') + '%',
                'event_number' : request.args.get('event_number', None),
                'event_status' : request.args.get('event_status', None),
                'start_date'   : request.args.get('start_date', None),
                'end_date'     : request.args.get('end_date', None),
                'is_exposed'   : request.args.get('is_exposed', None),
                'event_type'   : ast.literal_eval(request.args.get('event_type', None))
            }

            event_list = self.service.get_event_list(db, arguments)

        except Exception as e:
            traceback.print_exc()
            return jsonify({'message':e.message}), 400

        else:
            return jsonify(event_list), 200

        finally:
            db.close()
