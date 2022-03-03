import string
from random import randint, choice
from ChessViews import ChessViews


class VirtualController:
    def __init__(self):
        pass

    def display_interface(self):
        pass


class ChessMainController(VirtualController):
    def __init__(self, view):
        self.view = view

    def run(self):
        self.view.display_interface()
