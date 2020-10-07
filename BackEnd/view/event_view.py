import json

from flask import jsonify, request
from flask.views import MethodView

from werkzeug.utils import secure_filename

import config, connection, ast

import traceback

class PostEventView(MethodView):
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

            if 'button_name' not in data:
                data['button_name'] = []
            else:
                data['button_name'] = ast.literal_eval(data['button_name'])

            if 'product_ids' not in data:
                data['product_ids'] = []
            else:
                data['product_ids'] = ast.literal_eval(data['product_ids'])

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
                'button_names'              : data['button_name'],
                'product_ids'               : data['product_ids'],
                'mapped_product_count'      : len(data['product_ids'])
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
