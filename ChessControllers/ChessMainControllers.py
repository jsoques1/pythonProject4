import configparser
import logging
import time
from operator import itemgetter
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
        if self.current_tournament is not None:
            assert False
            # self.selected_tournament = tournament
        else:
            self.selected_tournament = tournament

    def get_selected_tournament(self):
        return self.selected_tournament

    def set_selected_players_list(self, selected_players_list):
        logging.debug('ChessMainControllers : set_selected_players_list')
        logging.info(f'ChessMainControllers : selected_players_list = {selected_players_list}')
        self.selected_players_list = selected_players_list

    def get_selected_players_list(self):
        return self.selected_players_list

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
            return 'No selected tournament'
        elif not selected_players_list:
            return 'No selected players'
        elif selected_tournament[3] > (len(selected_players_list) / 2):
            return f'nb of rounds ({selected_tournament[3]}) exceeds number of players couples'
        else:
            sorted_selected_players_list = sorted(selected_players_list, key=itemgetter(4), reverse=True)
            logging.info(f'ChessMainControllers : sorted_selected_players_list = {sorted_selected_players_list}')
            self.my_model.update_a_tournament_players_list(selected_tournament, sorted_selected_players_list)
            self.selected_players_list.clear()
            self.my_view.clear_player_view_tree_players_list_selection()
            return ''

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

    def get_rounds_matches_from_selected_tournament(self):
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
        matches_list = []
        for a_round in self.selected_rounds_list:
            for a_match in a_round[3]:
                matches_list.append([a_round[0], a_match[0][0], a_match[0][2], a_match[1][0], a_match[1][2]])
        return matches_list

    @staticmethod
    def get_current_time():
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
        self.players_score = self.my_model.get_participants_score(tournament)
        logging.info(f'ChessMainControllers : players = {players_list}')
        logging.info(f'ChessMainControllers : players_score = {self.players_score}')
        # if players_list and self.players_score:
        if players_list:
            if update_to_make:
                for current in range(len(players_list)):
                    players_list[current][4] = self.players_score[players_list[current][0]]
                logging.info(f'ChessMainControllers : players_list before sort : len = {len(players_list)} players_list = {players_list}')
                players_list = sorted(players_list, key=lambda x: float(x[4]), reverse=True)
                logging.info(f'ChessMainControllers : players_list after sort : len = {len(players_list)} players_list = {players_list}')

                self.players_couple_list = self.get_result_algorithm_swiss(players_list)
            else:
                nb_players_couple = int(len(players_list) / 2)
                self.players_couple_list = []

                for current in range(nb_players_couple):
                    opponent = current + nb_players_couple

                    first_player = [players_list[current][0], players_list[current][5], 0]
                    second_player = [players_list[opponent][0], players_list[opponent][5], 0]

                    self.players_couple_list.append(first_player)
                    self.players_couple_list.append(second_player)
                    self.players_couple_list_in_all_round.append([first_player, second_player])

        logging.info(f'ChessMainControllers : players couples in all rounds = {self.players_couple_list_in_all_round}')
        logging.info(f'ChessMainControllers : players couples = {self.players_couple_list}')
        logging.info(f'ChessMainControllers : self.selected_rounds_list = {self.selected_rounds_list}')

        return self.selected_rounds_list, self.players_couple_list, tournament

    def make_simplified_players_couples_list(self):
        logging.debug(f'ChessMainControllers : make_simplified_players_couples_list')
        players_couple_list = self.players_couple_list_in_all_round.copy()
        simplified_players_couple_list = []
        logging.info(f'ChessMainControllers : make_simplified_players_couples_list : players_couple_list={players_couple_list}')
        for couple_list in players_couple_list:
            logging.info(f'ChessMainControllers : make_simplified_players_couples_list : couple_list={couple_list}')
            first_player_id = couple_list[0][1]
            second_player_id = couple_list[1][1]
            simplified_players_couple_list.append([first_player_id, second_player_id])
        return simplified_players_couple_list

    def get_result_algorithm_swiss(self, players_list):
        logging.debug(f'ChessMainControllers : get_result_algorithm_swiss')
        logging.info(f'ChessMainControllers : get_result_algorithm_swiss: players_list={players_list}')
        simplified_players_couple_list = self.make_simplified_players_couples_list()
        logging.info(f'ChessMainControllers : get_result_algorithm_swiss: simplified_players_couple_list = {simplified_players_couple_list}')
        nb_players_couple = int(len(players_list) / 2)
        new_players_list = []
        opponents_list = [i+nb_players_couple for i in range(nb_players_couple)]
        logging.info(f'ChessMainControllers : opponents_list={opponents_list}')
        for current in range(nb_players_couple):
            for opponent in opponents_list:
                logging.info(f'ChessMainControllers : get_result_algorithm_swiss: current={current} opponent={opponent}')
                if ([players_list[current][5], players_list[opponent][5]] in simplified_players_couple_list) or \
                        ([players_list[opponent][5], players_list[current][5]] in simplified_players_couple_list):
                    continue
                else:
                    logging.info(f'ChessMainControllers : get_result_algorithm_swiss: couple found {players_list[current]} {players_list[opponent]}')

                    new_players_list.append(players_list[current])
                    new_players_list.append(players_list[opponent])
                    first_player = [players_list[current][0], players_list[current][5], players_list[current][4]]
                    second_player = [players_list[opponent][0], players_list[opponent][5], players_list[opponent][4]]
                    self.players_couple_list_in_all_round.append([first_player, second_player])
                    logging.info(f'ChessMainControllers : get_result_algorithm_swiss: players_list[current]={players_list[current]}')
                    logging.info(
                        f'ChessMainControllers : get_result_algorithm_swiss: players_list[opponent]={players_list[opponent]}')
                    opponents_list.remove(opponent)
                    break
        return new_players_list

    def set_player_id(self, player_id):
        self.player_id = player_id
        return self.player_id

    def get_player_id(self):
        self.player_id += 1
        return self.player_id

    def get_players_ordered_by_name(self):
        rounds_list, players_list, _ = self.get_rounds_players_from_selected_tournament()
        ordered_players_list = sorted(players_list, key=itemgetter(0))
        return ordered_players_list

    def get_players_ordered_by_rank(self):
        rounds_list, players_list, _ = self.get_rounds_players_from_selected_tournament()
        ordered_players_list = sorted(players_list, key=itemgetter(0))
        return ordered_players_list

    def get_all_tournaments(self):
        tournaments_list = self.load_tournaments_list()
        return tournaments_list

    def get_a_tournament_rounds(self):
        rounds_list, players_list, _ = self.get_rounds_players_from_selected_tournament()
        return rounds_list

    def get_a_tournament_matches(self):
        matches_list = self.get_rounds_matches_from_selected_tournament()
        return matches_list

    def get_participants_score(self):
        tournament = self.get_selected_tournament()
        players_score = self.my_model.get_participants_score(tournament)
        final_scores = []
        for key, value in players_score.items():
            final_scores.append([key, value])
        final_scores = sorted(final_scores, key=itemgetter(1), reverse=True)
        return final_scores

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
                                                          tournament[4], tournament[5], tournament[6],
                                                          participants_score=dict())
            model_tournaments_list.append(model_tournament)
        status = self.my_model.check_and_insert_tournaments_in_db(model_tournaments_list)
        return status

    def save_a_tournament(self, tournament):
        model_tournament = ChessMainModels.Tournament(tournament[0], tournament[1], tournament[2], tournament[3],
                                                      tournament[4], tournament[5], tournament[6],
                                                      participants_score=dict())
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
                logging.info(f'ChessMainControllers : update_a_match_results_list_round : player_key = {player_key}')
                logging.info(f'ChessMainControllers : update_a_match_results_list_round : a_match_result[3][2] = {a_match_result[3][2]}')
                logging.info(
                    f'ChessMainControllers : update_a_match_results_list_round : type(players_score) = '
                    f'{self.players_score}')
                logging.info(
                    f'ChessMainControllers : update_a_match_results_list_round : type(a_match_result) = {a_match_result}')
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
        self.set_tournament_id(len(tournaments_list))
        return tournaments_list

    def set_tournament_id(self, tournament_id):
        self.tournament_id = tournament_id
        return self.tournament_id

    def get_tournament_id(self):
        self.tournament_id += 1
        return self.tournament_id
