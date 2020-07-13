from threading import Thread
from event import Event
from event import EventType
from event_handler import EventHandler
from overrides import overrides
from flask import request
from flask import jsonify
from flask import send_file
from flask_cors import CORS

import pymysql
import os

class Server(EventHandler):

    def __init__(self, dispatcher, logger, app):
        super().__init__(dispatcher, logger)
        self._app = app
        self._app.add_url_rule('/speech', 'speech', self.handle_data,
                               methods=['POST'])
        self._app.add_url_rule('/result', 'result', self.handle_result,
                               methods=['GET'])
        CORS(self._app)

        self._server_thread = None
        self._run_server()

        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='root',
                                    db='emo_speech', charset='utf8', port=33906)

    def _run_server(self):
        self._server_thread = Thread(target=self._app.run,
                                     daemon=True)
        self._server_thread.start()

    @overrides
    def handle_event(self, event):
        if event.type == EventType.DATA_ARRIVED:
            pass
        elif event.type == EventType.RESULT_ARRIVED:
            pass

    def _handle_data_arrived(self, event):
        return

    def _handle_result_arrived(self):
        return

    def handle_data(self):
        uuid = request.form.get(key='uuid', type=str)
        request_time = request.form.get(key='request_time')
        speech = request.files['speech']
        emotion = request.form.get(key='emotion', type=str)
        intensity = request.form.get(key='intensity', type=float)
        print(uuid, request_time, emotion, intensity)

        # DB에 입력
        curs = self.conn.cursor()
        sql = """insert into InferenceStatus(uuid,request_time,status,emotion,intensity)
                values (%s, %s, %s, %s, %s)"""
        curs.execute(sql, (uuid, request_time, False, emotion, intensity))
        self.conn.commit()
        self.conn.close()

        # 파일 저장
        basepath = os.path.dirname(__file__)
        directory = os.path.join(basepath, 'inference', uuid)
        if not os.path.exists(directory):
                os.makedirs(directory)
        file_path = os.path.join(
                    basepath, 'inference', uuid, 'input.wav')
        speech.save(file_path)

        # 모델 data_manager 이벤트 발생
        event = Event(payload={'uuid':uuid, 'request_time':request_time, 'emotion':emotion, 'intensity':intensity}, type=EventType.DATA_ARRIVED)
        self.publish_event(event)
        return 'data arrived'

    def handle_result(self):
        uuid = request.form.get(key='uuid', type=str)
        request_time = request.form.get(key='request_time')

        curs = self.conn.cursor()
        sql = """select *
                from InferenceStatus
                where uuid=%s and request_time=%s"""
        curs.execute(sql, (uuid, request_time))
        result = curs.fetchone()
        status = result[2] # 0:False, 1:True
        emotion = result[3]
        intensity = result[4]
        print('상태', status, intensity)
        self.conn.commit()
        self.conn.close()

        # False이면
        if status==0:
            return False
        else: # True이면
            # 파일 경로
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(basepath, 'inference', uuid, emotion, f'{intensity}.mp3')
            print(file_path)
            return send_file(file_path, attachment_filename='result.mp3')
