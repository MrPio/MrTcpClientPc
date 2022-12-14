import json
import websocket
from service.recv_handler import RecvHandler

url = 'wss://mrpio-mrpowermanager.onrender.com/ws/'
local_url = 'ws://localhost:8000/ws/'


class WebsocketManager:

    def __init__(self,
                 token: str,
                 handler:RecvHandler,
                 trace: bool = True):
        self.handler=handler
        websocket.enableTrace(trace)
        self.ws = websocket.WebSocketApp(
            url=url + token,
            on_open=lambda _: self.__on_open(),
            on_message=lambda _, msg: self.__on_message(msg),
            on_error=lambda _, err: self.__on_error(err),
            on_close=lambda _: self.__on_close(),
        )

    def run(self):
        self.ws.run_forever()

    def send_string(self, msg: str):
        self.ws.send(msg.encode(), websocket.ABNF.OPCODE_BINARY)

    def send_json(self,msg:dict):
        msg_str=json.dumps(msg)
        self.send_string(msg_str)

    def send_bytes(self,msg:bytes):
        self.ws.send(msg,websocket.ABNF.OPCODE_BINARY)

    def __on_open(self):
        self.send_string('pc online')

    def __on_message(self, msg: bytes):
        self.handler.on_message(msg)


    def __on_error(self, err):
        print(err)

    def __on_close(self):
        print("### closed ###")
