from service.recv_handler import RecvHandler
from websocket_manager.websocket_manager import WebsocketManager

recv_handler = RecvHandler()
websocket_manager = WebsocketManager(
    token='111',
    handler=recv_handler,
    trace=True,
)

if __name__ == '__main__':
    websocket_manager.run()
