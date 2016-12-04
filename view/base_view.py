class BaseView:
    def __init__(self, controller):
        self._controller = controller
        self._controller.set_view(self)
