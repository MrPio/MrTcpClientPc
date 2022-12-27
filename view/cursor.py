from PyQt5.QtWidgets import QLabel


from view.my_main_window import MyMainWindow


class Cursor(MyMainWindow):

    def __init__(self):
        from main import ROOT_DIR
        super().__init__(ROOT_DIR + '/view/ui/cursor.ui')
        self.setMaximumWidth(64)
        self.setMaximumHeight(64)

    def getCursorLabel(self) -> QLabel:
        return self.cursorLabel
