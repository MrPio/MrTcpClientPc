import os
from threading import Thread

from PIL import Image
from pystray import Icon, Menu, MenuItem

from service.main_service import MainService

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

mainService = MainService.getInstance()
websocket_manager=mainService.websocket_manager


def start_tray():
    def stray_handler(_, item):
        if str(item) == 'Stream Webcam':
            mainService.open_stream('WEBCAM_RECV')
        elif str(item) == 'Stop Webcam':
            mainService.stop_thread()
        elif str(item) == 'Send ciao':
            websocket_manager.send_string('ciao!')
        elif str(item) == 'Exit':
            mainService.stop_thread()
            websocket_manager.ws.close()
            os._exit(1)

    def zoom_handler(_, item):
        val = float(str(item))
        websocket_manager.send_json({
            'type': 'command',
            'command_name': 'WEBCAM_ZOOM',
            'value': val
        })

    def flash_handler(_, item):
        websocket_manager.send_json({
            'type': 'command',
            'command_name': 'WEBCAM_FLASH',
            'value': 'on' if str(item) == 'on' else 'off'
        })

    def resolution_handler(_, item):
        websocket_manager.send_json({
            'type': 'command',
            'command_name': 'WEBCAM_RESOLUTION',
            'value': str(item)
        })

    def quality_handler(_, item):
        websocket_manager.send_json({
            'type': 'command',
            'command_name': 'WEBCAM_QUALITY',
            'value': int(str(item))
        })

    Icon(
        'MrTcp',
        Image.open("icon.ico"),
        menu=Menu(
            MenuItem('Stream Webcam', stray_handler),
            MenuItem('Stop Webcam', stray_handler),
            Menu.SEPARATOR,
            MenuItem('Send ciao', stray_handler),
            Menu.SEPARATOR,
            MenuItem(
                'Zoom',
                Menu(
                    MenuItem('0', zoom_handler),
                    MenuItem('0.15', zoom_handler),
                    MenuItem('0.3', zoom_handler),
                    MenuItem('0.45', zoom_handler),
                    MenuItem('0.6', zoom_handler),
                    MenuItem('0.75', zoom_handler),
                    MenuItem('1', zoom_handler),
                ),
            ),
            MenuItem(
                'Flash',
                Menu(
                    MenuItem('on', flash_handler),
                    MenuItem('off', flash_handler),
                ),
            ),
            MenuItem(
                'Resolution',
                Menu(
                    MenuItem('low', resolution_handler),
                    MenuItem('medium', resolution_handler),
                    MenuItem('high', resolution_handler),
                    MenuItem('veryHigh', resolution_handler),
                    MenuItem('ultraHigh', resolution_handler),
                    MenuItem('max', resolution_handler),
                ),
            ),
            MenuItem(
                'Quality',
                Menu(
                    MenuItem('0', quality_handler),
                    MenuItem('10', quality_handler),
                    MenuItem('20', quality_handler),
                    MenuItem('40', quality_handler),
                    MenuItem('60', quality_handler),
                    MenuItem('80', quality_handler),
                    MenuItem('90', quality_handler),
                    MenuItem('97', quality_handler),
                ),
            ),
            Menu.SEPARATOR,
            MenuItem('Exit', stray_handler),
        )
    ).run()


if __name__ == '__main__':
    Thread(target=start_tray).start()
    websocket_manager.run()
