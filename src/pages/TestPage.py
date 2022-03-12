import pages.MasterPage as MasterPage


class TestPage(MasterPage.MasterPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
