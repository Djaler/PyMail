class BaseController:
    def __init__(self):
        self._view = None
    
    def set_view(self, view):
        self._view = view
