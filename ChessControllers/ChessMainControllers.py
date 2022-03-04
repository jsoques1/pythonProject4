import logging
from ChessViews import ChessMainViews
from ChessModels import ChessMainModels


class VirtualController:
    def __init__(self):
        pass

    def run(self):
        pass


class ChessMainController(VirtualController):
    def __init__(self, view, model):
        super().__init__()
        self.my_view = view
        self.my_model = model

    def run(self):
        self.my_view.set_my_controller(self)
        self.my_model.set_my_controller(self)
        self.my_view.display_interface()

    def save_players_list(self, players_list):
        status = self.my_model.check_and_insert_players_in_db(players_list)
        return status

    def load_players_list(self):
        logging.debug('load_players_list')
        result = self.my_model.load_players_in_db()
        return result
