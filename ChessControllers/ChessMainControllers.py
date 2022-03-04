import logging
from operator import itemgetter
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
        model_players_list = []
        for player in players_list:
            model_player = ChessMainModels.Player(player[0], player[1], player[2], player[3], player[4])
            model_players_list.append(model_player)
        status = self.my_model.check_and_insert_players_in_db(model_players_list)
        return status

    def load_players_list(self):
        logging.debug('load_players_list')
        model_players_list = self.my_model.load_players_in_db()
        players_list = []
        for model_player in model_players_list:
           players_list.append(model_player.unserialize())
        return players_list

    def sort_players_list_by_name(self, players_list):
        return sorted(players_list, key=lambda x: (x[0] == "", x[0].lower()))

    def sort_players_list_by_rank(self, players_list):
        return sorted(players_list, key=lambda x: (x[4] == "", x[4].lower()))
