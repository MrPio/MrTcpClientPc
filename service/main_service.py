import json
import time
from threading import Thread

import winotify

from checksum.checksum_check import ChecksumCheck
from checksum.md5_checksum_check import MD5ChecksumCheck
from service.recv_close_handler.recv_close_handler import RecvCloseHandler
from service.recv_close_handler.recv_file import RecvFile
from service.recv_open_handler.recv_gyroscope import RecvGyroscope
from service.recv_open_handler.recv_microphone import RecvMicrophone
from service.recv_open_handler.recv_open_handler import RecvOpenHandler
from service.recv_open_handler.recv_webcam import RecvWebcam
from service.send_close_handler.send_close_handler import SendCloseHandler
from service.send_open_handler.send_open_handler import SendOpenHandler
from service.send_open_handler.send_webcam import SendWebcam
from websocket_manager.websocket_manager import WebsocketManager


class MainService:
    checksum_check: ChecksumCheck = MD5ChecksumCheck()

    def __init__(self, websocket_manager: WebsocketManager):
        websocket_manager.on_message = self.__on_message
        self.websocket_manager = websocket_manager
        self.current_command: dict | None = None
        self.last_json: dict | None = None
        self.commands_queue: list[dict] = []
        self.recv_close_handlers: dict[str, RecvCloseHandler] = {
            'FILE': RecvFile(),
        }
        self.recv_open_handlers: dict[str, RecvOpenHandler] = {
            'WEBCAM_RECV': RecvWebcam(),
            'MIC_RECV': RecvMicrophone(),
            'GYRO_RECV': RecvGyroscope(),
        }
        self.send_close_handlers: dict[str, SendCloseHandler] = {

        }
        self.send_open_handlers: dict[str, SendOpenHandler] = {
            'WEBCAM_SEND': SendWebcam(),
        }
        self.thread: Thread | None = None
        self.last_notify: int = time.time_ns()

    # ========== private ====================
    def __process_json(self, msg: dict):
        print('__process_json:', msg)
        self.last_json = msg
        if msg['type'] == 'command':
            # if I am already handling a command, I store the new one in the queue
            if self.current_command is not None and not 'stop' in msg.keys():
                self.commands_queue.append(msg)
                return

            self.current_command = msg
            cmd = msg['command_name']

            if 'stop' in msg.keys():
                self.current_command = None

            # initialize the handler if it is a RECV_CLOSE one
            if cmd in self.recv_close_handlers.keys():
                self.recv_close_handlers[cmd].initialize(msg)

            # initialize the handler if it is a RECV_OPEN one
            if cmd in self.recv_open_handlers.keys():
                self.recv_open_handlers[cmd].initialize()

            # close the handler if it is a RECV_OPEN one and the cmd asks to close
            elif cmd in self.recv_open_handlers.keys():
                if 'stop' in msg.keys():
                    self.recv_open_handlers[cmd].stop()

    def __process_bytes(self, msg: bytes):
        if self.current_command is None:
            return
        cmd = self.current_command['command_name']
        if cmd in self.recv_close_handlers.keys():
            self.recv_close_handlers[cmd].process(msg, self.last_json['md5'])
        elif cmd in self.recv_open_handlers.keys():
            self.websocket_manager.send_string('PKG_RECV')
            self.recv_open_handlers[cmd].process(msg)

    def __process_string(self, msg: str):
        if time.time_ns() - self.last_notify < 0.3e9:
            return
        self.last_notify = time.time_ns()
        from main import ROOT_DIR
        notifica = winotify.Notification(
            app_id='MrTcp',
            title='You received a message',
            msg=msg,
            icon=ROOT_DIR + '/icon.ico',
            duration='short',
        )
        notifica.set_audio(winotify.audio.Default, False)
        notifica.show()

    def __on_message(self, msg: bytes):
        # try to convert to json
        try:
            self.__process_json(json.loads(msg))
            return
        except Exception:
            pass
        # if I am not handling a command
        if self.current_command is None:
            # try to convert to string
            try:
                self.__process_string(msg.decode())
                return
            except Exception:
                pass
        # use as binary
        self.__process_bytes(msg)
        pass

    # ========== public ======================
    def stop_thread(self):
        if not self.thread is None:
            self.thread.join()

    def open_stream(self, cmd: str):
        if not cmd in self.send_open_handlers:
            return
        handler = self.send_open_handlers[cmd]
        self.websocket_manager.send_json(handler.send_start())
        time.sleep(0.1)

        def send():
            while True:
                self.websocket_manager.send_bytes(handler.send())
                # time.sleep(0.05)

        self.thread = Thread(target=send)
        self.thread.start()
