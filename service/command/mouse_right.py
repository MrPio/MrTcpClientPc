import pyautogui

from service.command.command import Command


class MouseRight(Command):
    def execute(self, cmd: dict):
        super().execute(cmd)
        pyautogui.click(button='right')