import pyautogui

from service.command.command import Command


class MouseMiddle(Command):
    def execute(self, cmd: dict):
        super().execute(cmd)
        pyautogui.click(button='middle')