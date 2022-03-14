import configparser
import logging
import time
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
        self.is_debug = ChessMainController.read_controllers_section_config_file()
        self.my_view = view
        self.my_model = model
        self.player_id = 0
        self.tournament_id = 0
        self.selected_players_list = []
        self.selected_rounds_list = []
        self.players_score = dict()
        self.players_couple_list = []
        self.players_couple_list_in_all_round = []
        self.selected_tournament = None
        self.current_tournament = None

    def run(self):
        self.my_view.set_my_controller(self)
        self.my_model.set_my_controller(self)
        self.my_view.display_interface()

    def set_selected_tournament(self, tournament):
        logging.debug('ChessMainControllers : set_selected_tournament')
        logging.info(f'ChessMainControllers : {tournament}')
        if self.current_tournament != None:
            assert False
            # self.selected_tournament = tournament
        else:
            self.selected_tournament = tournament

    def get_selected_tournament(self):
        return self.selected_tournament

    def set_selected_players_list(self, selected_players_list=[]):
        logging.debug('ChessMainControllers : set_selected_players_list')
        logging.info(f'ChessMainControllers : selected_players_list = {selected_players_list}')
        self.selected_players_list = selected_players_list

    def get_selected_players_list(self):
        return(self.selected_players_list)

    def set_tournament_completed(self):
        self.selected_players_list = []
        self.selected_rounds_list = []
        self.players_score = dict()
        self.players_couple_list = []
        self.players_couple_list_in_all_round = []
        self.selected_tournament = None

    def assign_selected_players_to_selected_tournament(self):
        logging.debug('ChessMainControllers : assign_selected_players_to_selected_tournament')
        selected_tournament = self.get_selected_tournament()
        selected_players_list = self.get_selected_players_list()
        if selected_tournament is None:
            return('No selected tournament')
        elif selected_players_list == []:
            return('No selected players')
        else:
            sorted_selected_players_list = sorted(selected_players_list, key=itemgetter(4), reverse=True)
            logging.info(f'ChessMainControllers : sorted_selected_players_list = {sorted_selected_players_list}')
            self.my_model.update_a_tournament_players_list(selected_tournament, sorted_selected_players_list)
            self.selected_players_list.clear()
            return('')

    def get_rounds_players_from_selected_tournament(self):
        logging.debug('ChessMainModels : get_rounds_players_from_selected_tournament')
        selected_tournament = self.get_selected_tournament()
        if selected_tournament is None:
            return [], [], None
        # elif self.players_couple_list_in_all_round:
        #     pass
        else:
            self.selected_rounds_list, self.selected_players_list = self.my_model.get_tournament_rounds_players_list(selected_tournament)
            logging.info(f'ChessMainControllers : rounds_list = {self.selected_rounds_list}')
            logging.info(f'ChessMainControllers : players_list = {self.selected_players_list}')
        return self.selected_rounds_list, self.selected_players_list, selected_tournament

    def get_current_time(self):
        return time.strftime(format("%H:%M:%S"))

    def get_max_rounds_number(self):
        logging.debug('ChessMainModels : get_max_rounds_number')
        selected_tournament = self.get_selected_tournament()
        max_rounds_number = selected_tournament[3]
        logging.info(f'ChessMainControllers : max rounds number = {max_rounds_number}')
        return max_rounds_number

    def get_rounds_players_couple_list(self, update_to_make=False):
        logging.debug('ChessMainControllers : get_rounds_players_couple_list')
        self.selected_rounds_list, players_list, tournament = self.get_rounds_players_from_selected_tournament()
        if tournament is None:
            return [], [], None
        self.players_score = self.my_model.get_players_score(tournament)
        logging.info(f'ChessMainControllers : players = {players_list}')
        logging.info(f'ChessMainControllers : players_score = {self.players_score}')
        # if players_list and self.players_score:
        if players_list:
            if self.players_score:
                if update_to_make:
                    for current in range(len(players_list)):
                        players_list[current][4] = self.players_score[players_list[current][0]]
                    logging.info(f'ChessMainControllers : players_list before sort : len = {len(players_list)} players_list = {players_list}')
                    players_list = sorted(players_list, key=lambda x: float(x[4]), reverse=True)
                    logging.info(f'ChessMainControllers : players_list after sort : len = {len(players_list)} players_list = {players_list}')

                nb_players_couple = int(len(players_list) / 2)
                self.players_couple_list = []
                for current in range(nb_players_couple):
                    opponent = current + nb_players_couple
                    if update_to_make:
                        first_player = [players_list[current][0], players_list[current][5], players_list[current][4]]
                        second_player = [players_list[opponent][0], players_list[opponent][5], players_list[opponent][4]]
                    else:
                        first_player = [players_list[current][0], players_list[current][5], 0]
                        second_player = [players_list[opponent][0], players_list[opponent][5], 0]

                    self.players_couple_list.append(first_player)
                    self.players_couple_list.append(second_player)
                    self.players_couple_list_in_all_round.append([first_player, second_player])
                logging.info(f'ChessMainControllers : players couples in all rounds = {self.players_couple_list_in_all_round}')
                logging.info(f'ChessMainControllers : players couples = {self.players_couple_list}')
                return self.selected_rounds_list, self.players_couple_list, tournament
            else:
                logging.info(f'ChessMainControllers : get_rounds_players_couple_list - self.selected_rounds_list \
= {self.selected_rounds_list} self.players_couple_list = {self.players_couple_list}')
                return [], [], None
        else:
            logging.debug('ChessMainControllers : get_rounds_players_couple_list - Deadly case (2)')
            return [], [], None

    def set_player_id(self, player_id):
        self.player_id = player_id
        return self.player_id

    def get_player_id(self):
        self.player_id += 1
        return self.player_id

    @staticmethod
    def read_controllers_section_config_file():
        logging.debug('ChessMainControllers : read_views_section_config_file')
        config = configparser.ConfigParser()
        config.read('MyChessApp.ini')
        is_debug = config['controllers']['is_debug']
        return is_debug

    def get_dummy_players_list(self):
        dummy_players_list = [('Messi', 'Lionel', '07/03/1984', 'Male', 1000, self.get_player_id()),
            ('Bronze', 'Lucy', '07/02/1990', 'Female', 2000, self.get_player_id()),
            ('Greenwood', 'Alex', '07/02/1996', 'Female', 1000, self.get_player_id()),
            ('Hegerberg', 'Ada', '07/02/1998', 'Female', 1000, self.get_player_id()),
            ('Ronaldo', 'Cristiano', '07/02/1990', 'Male', 4000, self.get_player_id()),
            ('Loris', 'Hugo', '07/02/1997', 'Male', 3000, self.get_player_id()),
            ('Weir', 'Stephanie', '07/02/2000', 'Female', 1000, self.get_player_id()),
            ('Bouhaddi', 'Sarah', '07/02/1986', 'Female', 5000, self.get_player_id())
        ]

        self.save_players_list(dummy_players_list)
        return dummy_players_list

    def save_players_list(self, players_list):
        model_players_list = []
        for player in players_list:
            model_player = ChessMainModels.Player(player[0], player[1], player[2], player[3], player[4], player[5])
            model_players_list.append(model_player)
        status = self.my_model.check_and_insert_players_in_db(model_players_list)
        return status

    def save_a_player(self, player):
        model_player = ChessMainModels.Player(player[0], player[1], player[2], player[3], player[4], player[5])
        status = self.my_model.check_and_insert_a_player_in_db(model_player)
        return status

    def update_a_player_rank(self, player, new_rank):
        model_player = ChessMainModels.Player(player[0], player[1], player[2], player[3], player[4], player[5])
        status = self.my_model.check_and_udate_a_player_rank_in_db(model_player)
        return status

    def load_players_list(self):
        logging.debug('ChessMainControllers : load_players_list')
        model_players_list = self.my_model.load_players_in_db()
        players_list = []
        for model_player in model_players_list:
           players_list.append(model_player.unserialize())
        return players_list

    def get_dummy_tournaments_list(self):
        dummy_tournaments_list = [('Toronto tournament', 'Toronto', '07/03/1984',  4, 'Blitz', 'Bitz tournament',
                               self.get_tournament_id()),
                              ('Paris tournament', 'Paris', '07/03/1984', 3, 'Bullet', 'Bullet tournament',
                               self.get_tournament_id()),
                              ('Milan tournament', 'Milan', '07/03/1984', 2, 'Fast', 'Fast tournament',
                               self.get_tournament_id()),
                             ]

        self.save_tournaments_list(dummy_tournaments_list)
        return dummy_tournaments_list

    def save_tournaments_list(self, tournaments_list):
        model_tournaments_list = []
        for tournament in tournaments_list:
            model_tournament = ChessMainModels.Tournament(tournament[0], tournament[1], tournament[2], tournament[3],
                                                          tournament[4], tournament[5], tournament[6])
            model_tournaments_list.append(model_tournament)
        status = self.my_model.check_and_insert_tournaments_in_db(model_tournaments_list)
        return status

    def save_a_tournament(self, tournament):
        print(tournament)
        model_tournament = ChessMainModels.Tournament(tournament[0], tournament[1], tournament[2], tournament[3],
                                                      tournament[4], tournament[5], tournament[6])
        status = self.my_model.check_and_insert_a_tournament_in_db(model_tournament)
        return status

    def update_a_tournament_players_list(self, tournament, players_list):
        model_tournament = ChessMainModels.Tournament(tournament[0], tournament[1], tournament[2], tournament[3],
                                                      tournament[4], tournament[5], tournament[6])
        status = self.my_model.update_a_tournament_players_list(model_tournament, players_list)
        return status

    def update_a_match_results_list_round(self, round_number, round_start_time, round_end_time, match_results_list):
        logging.debug('ChessMainControllers : update_a_match_results_list_round')
        match_list = []
        selected_tournament = self.get_selected_tournament()
        logging.info(f'ChessMainControllers : len = {len(match_results_list)} match_results_list ={match_results_list}')
        for a_match_result in match_results_list:
            match_list.append([a_match_result[3], a_match_result[4]])
            player_key = a_match_result[3][0]
            if player_key in self.players_score:
                self.players_score[player_key] = float(self.players_score[player_key]) + float(a_match_result[3][2])
            else:
                self.players_score[player_key] = float(a_match_result[3][2])

            player_key = a_match_result[4][0]
            if player_key in self.players_score:
                self.players_score[player_key] = float(self.players_score[player_key]) + float(a_match_result[4][2])
            else:
                self.players_score[player_key] = float(a_match_result[4][2])

        status = self.my_model.update_a_tournament_round(selected_tournament, round_number, round_start_time,
                                                         round_end_time, match_list, self.players_score)
        return round_number, status

    def load_tournaments_list(self):
        logging.debug('ChessMainControllers : load_tournaments_list')
        model_tournaments_list = self.my_model.load_tournaments_in_db()
        tournaments_list = []
        for model_tournament in model_tournaments_list:
            tournaments_list.append(model_tournament.unserialize())
            logging.info(f'model_tournament = {model_tournament}')
        return tournaments_list

    def set_tournament_id(self, tournament_id):
        self.tournament_id = tournament_id
        return self.tournament_id

    def get_tournament_id(self):
        self.tournament_id += 1
        return self.tournament_id
