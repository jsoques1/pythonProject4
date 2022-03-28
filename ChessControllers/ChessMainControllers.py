import configparser
import copy
import logging
import re
import time
from operator import itemgetter
from ChessModels import ChessMainModels


class VirtualController:
    def __init__(self):
        pass

    def run(self):
        pass


class ChessPlayers:
    def __init__(self):
        self.players = dict()

    def add_players(self, tournament_id, players):
        logging.debug('ChessPlayers: add_players')
        logging.info(f'ChessPlayers: add_players: players={players}')
        self.players[tournament_id] = players
        logging.info(f'ChessPlayers: add_matches: matches={self.players}')

    def get_players(self, tournament_id):
        logging.debug('ChessPlayers: get')
        logging.info(f'ChessPlayersChessPlayers: get: players={self.players.get(tournament_id)}')
        return self.players.get(tournament_id)


class ChessRoundId:
    def __init__(self):
        self.tournament_round_id = dict()

    def get_tournament_round_id(self, tournament_id):
        logging.debug('ChessRoundId: get_tournament_round_id')
        if not self.tournament_round_id.get(tournament_id):
            self.tournament_round_id[tournament_id] = 1
        return self.tournament_round_id[tournament_id]

    def set_tournament_round_id(self, tournament_id, round_id):
        logging.debug('ChessRoundId: set_tournament_round_id')
        if not self.tournament_round_id.get(tournament_id):
            self.tournament_round_id[tournament_id] = round_id
        else:
            self.tournament_round_id[tournament_id] = round_id
        return self.tournament_round_id[tournament_id]

    def increment_tournament_round_id(self, tournament_id):
        logging.debug('ChessRoundId: increment_tournament_round_id')
        if not self.tournament_round_id.get(tournament_id):
            self.tournament_round_id[tournament_id] = 1
        else:
            self.tournament_round_id[tournament_id] += 1
        logging.debug('ChessRoundId: increment_tournament_round_id: round_id= ' +
                      f'{self.tournament_round_id[tournament_id]}')
        return self.tournament_round_id[tournament_id]

    def display(self):
        logging.debug('ChessRoundId: display')
        for key, value in self.tournament_round_id.items():
            logging.info(f'ChessRoundId: display: key={key} value={value}')


class ChessMatches:
    def __init__(self):
        self.matches = dict()

    def set(self, tournament_id, rounds):
        self.matches[tournament_id] = ChessMatches.make_flat(copy.deepcopy(rounds))

    def get_nb_matches(self, tournament_id):
        return len(self.matches.get(tournament_id))

    def get_all_matches_as_list(self, tournament_id):
        logging.debug('ChessMatches: get_matches')
        if self.matches.get(tournament_id):
            all_matches_list = []
            all_rounds = self.get_all_rounds(tournament_id)
            for a_round in all_rounds:
                logging.info(f'ChessMatches: get_matches: rounds={a_round}')
                round_number = a_round[0]
                for a_match in a_round[3]:
                    all_matches_list.append([round_number, a_match[0][0], a_match[0][2],
                                             a_match[1][0], a_match[1][2]])
            return all_matches_list
        else:
            return []

    @staticmethod
    def make_flat(rounds):
        logging.debug('ChessMatches: make_flat')
        logging.info(f'ChessMatches: make_flat: rounds={copy.deepcopy(rounds)}')
        new_matches = []
        for a_round in rounds:
            round_number = a_round[0]
            round_start_time = a_round[1]
            round_end_time = a_round[2]
            matches = a_round[3]
            for a_match in matches:
                logging.info(f'ChessMatches: make_flat: a_match={a_match}')
                first_player = a_match[0]
                second_player = a_match[1]
                a_new_match = [round_number, round_start_time, round_end_time, first_player, second_player]
                logging.info(f'ChessMatches: make_flat: a_new_match={a_new_match}')
                new_matches.append(a_new_match)
        return new_matches

    def add_matches(self, tournament_id, round_number, match_results_list):
        logging.debug('ChessMatches: add_matches')
        logging.info(f'ChessMatches: add_matches: tournament_id={tournament_id}')
        logging.info(f'ChessMatches: add_matches: round_number={round_number}')
        logging.info(f'ChessMatches: add_matches: match_results_list={match_results_list}')
        if not self.matches.get(tournament_id):
            logging.info('ChessMatches: add_matches: case(1)')
            self.matches[tournament_id] = copy.deepcopy(match_results_list)
        else:
            logging.info('ChessMatches: add_matches: case(2)')
            new_match_results_list = self.matches[tournament_id]
            new_match_results_list += copy.deepcopy(match_results_list)
            self.matches[tournament_id] = new_match_results_list

        logging.info(f'ChessMatches: add_matches: self.matches[{tournament_id}]={self.matches[tournament_id]}')

    def remove_matches_of_a_round(self, tournament_id, round_number):
        logging.debug('ChessMatches: remove_matches_of_a_round')
        matches = self.matches.get(tournament_id)
        if matches:
            logging.debug(f'ChessMatches: remove_matches_of_a_round: matches={matches}')
            for a_match in matches:
                if a_match[0] == round_number:
                    matches.remove(a_match)

    @staticmethod
    def compact_a_round(backup_round):
        logging.debug('ChessMatches: compact_a_round')
        logging.info(f'ChessMatches: compact_a_round: backup_round={backup_round}')
        retval = []
        if backup_round:
            last_match = backup_round[-1]
            match_couples = []
            for a_match in backup_round:
                a_couple = [a_match[3], a_match[4]]
                if not (a_couple in match_couples):
                    match_couples.append(a_couple)
            first_match = backup_round[0]
            round_number = first_match[0]
            start_time = first_match[1]
            end_time = last_match[2]
            retval = [round_number, start_time, end_time, match_couples]
        logging.info(f'ChessMatches: compact_a_round: retval={retval}')
        return retval

    def get(self):
        return self.matches

    def get_all_rounds(self, tournament_id):
        logging.debug('ChessMatches: get_all_rounds')
        matches = copy.deepcopy(self.matches.get(tournament_id))
        logging.info(f'ChessMatches: get_all_rounds: matches={matches}')
        if matches:
            backup_round = []
            all_rounds = []
            for a_match in matches:
                logging.info(f'ChessMatches: get_all_rounds: a_match={a_match}')
                if (not backup_round) or (a_match[0] == backup_round[0][0]):
                    backup_round.append(a_match)
                else:
                    a_round = ChessMatches.compact_a_round(backup_round)
                    logging.info(f'ChessMatches: get_all_rounds: a_round(1)={a_round}')
                    all_rounds.append(a_round)
                    backup_round.clear()
                    backup_round.append(a_match)

            if backup_round:
                a_round = ChessMatches.compact_a_round(backup_round)
                logging.info(f'ChessMatches: get_all_rounds: a_round(2)={a_round}')
                all_rounds.append(a_round)

            logging.info(f'ChessMatches: get_all_rounds: all_rounds={all_rounds}')
            return all_rounds
        else:
            return []

    def __str__(self):
        return str(self.matches)


class ChessPlayersScore:
    def __init__(self):
        self.players_score = dict()

    def update_a_score(self, player, score):
        logging.debug('ChessPlayersScore: update_a_score')
        logging.info(f'ChessPlayersScore: update_a_score: player={player} score={score}')
        if not self.players_score.get(player):
            self.players_score[player] = float(score)
        else:
            self.players_score[player] += float(score)

    def set(self, players_score):
        logging.debug('ChessPlayersScore: set')
        logging.info(f'ChessPlayersScore: set: players_score={players_score}')
        self.players_score = players_score

    def get(self):
        logging.debug('ChessPlayersScore: get')
        return self.players_score

    def get_score(self, player):
        logging.debug('ChessPlayersScore: get_score')
        logging.info(f'ChessPlayersScore: get_score: player={player} score={self.players_score.get(player)}')
        return self.players_score.get(player)

    def __str__(self):
        return str(self.players_score)


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
        self.players_couple_list = []
        self.all_matches = []
        self.selected_tournament = None
        self.players_score = ChessPlayersScore()
        self.matches = ChessMatches()
        self.round_id = ChessRoundId()

    def run(self):
        self.my_view.set_my_controller(self)
        self.my_model.set_my_controller(self)
        self.my_view.display_interface()

    def get_all_matches(self):
        return self.all_matches

    def get_all_matches_as_list(self):
        selected_tournament = self.get_selected_tournament()
        if selected_tournament:
            return self.matches.get_all_matches_as_list(selected_tournament[6])

    def get_nb_matches(self, tournament_id):
        return self.matches.get_nb_matches(tournament_id)

    def set_selected_tournament(self, tournament):
        logging.debug('ChessMainControllers: set_selected_tournament')
        logging.info(f'ChessMainControllers: set_selected_tournament: {tournament}')
        self.selected_tournament = tournament
        if tournament:
            self.players_score.set(self.retrieve_participants_score())

    def get_selected_tournament(self):
        return self.selected_tournament

    def set_selected_players_list(self, selected_players_list):
        logging.debug('ChessMainControllers: set_selected_players_list')
        logging.info(f'ChessMainControllers: selected_players_list = {selected_players_list}')
        self.selected_players_list = selected_players_list

    def get_selected_players_list(self):
        logging.debug('ChessMainControllers: get_selected_players_list')
        logging.info(f'ChessMainControllers: get_selected_players_list = {self.selected_players_list}')
        return self.selected_players_list

    def get_tournament_round_id(self):
        logging.debug('ChessMainControllers: get_tournament_round_id')
        tournament_round_id = 1
        selected_tournament = self.get_selected_tournament()
        if selected_tournament:
            tournament_id = selected_tournament[6]
            tournament_round_id = self.round_id.get_tournament_round_id(tournament_id)
        self.round_id.display()
        return tournament_round_id

    def initialize_tournament_round_id(self, tournament_id, round_id):
        logging.debug('ChessMainControllers: initialize_tournament_round_id')
        tournament_round_id = self.round_id.set_tournament_round_id(tournament_id, round_id)
        self.round_id.display()
        return tournament_round_id

    def set_tournament_round_id(self, round_id):
        logging.debug('ChessMainControllers: set_tournament_round_id')
        tournament_round_id = round_id
        selected_tournament = self.get_selected_tournament()
        if selected_tournament:
            tournament_id = selected_tournament[6]
            tournament_round_id = self.round_id.set_tournament_round_id(tournament_id, round_id)
        self.round_id.display()
        return tournament_round_id

    def increment_tournament_round_id(self):
        logging.debug('ChessMainControllers: increment_tournament_round_id')
        tournament_round_id = 1
        selected_tournament = self.get_selected_tournament()
        if selected_tournament:
            tournament_id = selected_tournament[6]
            tournament_round_id = self.round_id.increment_tournament_round_id(tournament_id)
        logging.debug(f'ChessMainControllers: increment_tournament_round_id: tournament_id={tournament_id} ' +
                      f'round_id={tournament_round_id}')
        self.round_id.display()
        return tournament_round_id

    def set_tournament_completed(self):
        self.selected_players_list = []
        self.selected_rounds_list = []
        self.players_couple_list = []
        self.all_matches = []

    def update_score(self,  a_match):
        logging.debug('ChessMainControllers: update_score')
        logging.info(f'ChessMainControllers: a_match ={a_match}')

        player_key = a_match[3][0]
        first_score = a_match[3][2]

        self.players_score.update_a_score(player_key, first_score)

        player_key = a_match[4][0]
        second_score = a_match[4][2]

        self.players_score.update_a_score(player_key, second_score)
        logging.info(f'ChessMainControllers: players_score ={self.players_score.get()}')

    def backup_a_round(self, round_number, round_end_time, match_results_list, tournament_id=None):
        logging.debug('ChessMainControllers: backup_a_round')
        logging.info(f'ChessMainControllers: backup_a_round: round_number={round_number}')
        logging.info(f'ChessMainControllers: backup_a_round: round_end_time: [{round_end_time}]')
        logging.info(f'ChessMainControllers: backup_a_round: match_results_list: {match_results_list}')
        if not tournament_id:
            selected_tournament = self.get_selected_tournament()
            tournament_id = selected_tournament[6]

        new_match_results_list = copy.deepcopy(match_results_list)

        for match in new_match_results_list:
            match[2] = round_end_time
            logging.info(f'ChessMainControllers: backup_a_round: match={match}')

        logging.info(f'ChessMainControllers: backup_a_round: new_match_results_list: {new_match_results_list}')
        self.matches.add_matches(tournament_id, round_number, new_match_results_list)

    def save_current_state(self):
        logging.debug('ChessMainControllers: save_current_state')
        logging.info(f'ChessMainControllers: save_current_state: matches={self.matches}')
        selected_tournament = self.get_selected_tournament()
        logging.info(f'ChessMainControllers: save_current_state: selected_tournament={selected_tournament}')
        tournament_id = selected_tournament[6]
        logging.info(f'ChessMainControllers: save_current_state: tournament_id={tournament_id}')
        all_rounds = self.matches.get_all_rounds(tournament_id)
        self.my_model.update_a_tournament_round(tournament_id, all_rounds, self.players_score.get())

    def assign_selected_players_to_selected_tournament(self):
        logging.debug('ChessMainControllers: assign_selected_players_to_selected_tournament')
        selected_tournament = self.get_selected_tournament()
        selected_players_list = self.get_selected_players_list()
        if selected_tournament is None:
            return 'No selected tournament'
        elif not selected_players_list:
            return 'No selected players'
        else:
            sorted_selected_players_list = sorted(selected_players_list, key=itemgetter(4), reverse=True)
            logging.info(f'ChessMainControllers: sorted_selected_players_list = {sorted_selected_players_list}')
            self.my_model.update_a_tournament_players_list(selected_tournament, sorted_selected_players_list)
            self.selected_players_list.clear()
            self.my_view.clear_player_view_tree_players_list_selection()
            return ''

    def get_all_rounds(self, tournament_id):
        return self.matches.get_all_rounds(tournament_id)

    def get_rounds_and_players(self):
        logging.debug('ChessMainModels: get_rounds_and_players')
        selected_tournament = self.get_selected_tournament()
        if selected_tournament is None:
            return [], []
        else:
            self.selected_rounds_list, self.selected_players_list, _ = \
                self.my_model.get_rounds_and_players_and_score(selected_tournament)
            logging.info(f'ChessMainControllers: rounds_list = {self.selected_rounds_list}')
            logging.info(f'ChessMainControllers: players_list = {self.selected_players_list}')
        return self.selected_rounds_list, self.selected_players_list

    def get_players_and_matches(self):
        logging.debug('ChessMainModels: get_players_and_matches')
        selected_tournament = self.get_selected_tournament()
        if selected_tournament is None:
            return [], []
        else:
            self.selected_rounds_list, self.selected_players_list, _ = \
                self.my_model.get_rounds_and_players_and_score(selected_tournament)
            logging.info(f'ChessMainControllers: get_players_and_matches: rounds_list = {self.selected_rounds_list}')
            logging.info(f'ChessMainControllers: get_players_and_matches: players_list = {self.selected_players_list}')

        matches_list = []
        for a_round in self.selected_rounds_list:
            for a_match in a_round[3]:
                matches_list.append([a_round[0], a_match[0][0], a_match[0][2], a_match[1][0], a_match[1][2]])
        return self.selected_players_list, matches_list

    @staticmethod
    def get_current_date_time():
        return time.strftime("%d/%m/%Y  -  %H:%M:%S")

    def get_max_rounds_number(self):
        logging.debug('ChessMainControllers: get_max_rounds_number')
        selected_tournament = self.get_selected_tournament()
        max_rounds_number = selected_tournament[3]
        logging.info(f'ChessMainControllers: max rounds number = {max_rounds_number}')
        return max_rounds_number

    def get_nb_matches_per_round(self):
        tournament = self.get_selected_tournament()
        nb_players = len(self.selected_players_list)
        if tournament:
            return int(nb_players / 2)
        else:
            return 0

    def is_max_rounds_number_reached(self):
        logging.debug('ChessMainControllers: is_max_rounds_number_reached')

        logging.info('ChessMainControllers: is_max_rounds_number_reached: ' +
                     f'selected_rounds_list={self.selected_rounds_list}')
        logging.info('ChessMainControllers: is_max_rounds_number_reached: ' +
                     f'get_max_rounds_number={self.get_max_rounds_number()}')

        if len(self.selected_rounds_list) == self.get_max_rounds_number():
            return True
        else:
            return False

    def is_last_round_nb_matches_reached(self):
        logging.debug('ChessMainControllers: is_last_round_nb_matches_reached')

        logging.info('ChessMainControllers: is_last_round_nb_matches_reached: ' +
                     f'self.selected_rounds_list[-1][3]={self.selected_rounds_list[-1][3]}')
        logging.info('ChessMainControllers: is_last_round_nb_matches_reached: ' +
                     f'get_nb_matches_per_round={self.get_nb_matches_per_round()}')
        if len(self.selected_rounds_list[-1][3]) == self.get_nb_matches_per_round():
            return True
        else:
            return False

    def is_last_round_reached_and_end_time_stamped(self):
        logging.debug('ChessMainControllers: is_last_round_reached_and_end_time_stamped')
        if self.selected_rounds_list and self.selected_rounds_list[-1]:
            logging.info('ChessMainControllers: is_last_round_reached_and_end_time_stamped: ' +
                         f'self.selected_rounds_list[-1][0]={self.selected_rounds_list[-1][0]}')
            logging.info('ChessMainControllers: is_last_round_reached_and_end_time_stamped: ' +
                         f'self.selected_rounds_list[-1][2]={self.selected_rounds_list[-1][2]}')
            round_id = int(re.findall(r"\d+", self.selected_rounds_list[-1][0])[0])
            self.set_tournament_round_id(round_id)
            if (round_id == self.get_max_rounds_number()) and self.selected_rounds_list[-1][2]:
                return True
            # elif self.selected_rounds_list[-1][2]:
            #     self.increment_tournament_round_id()
            # else:
            #     return False
        else:
            return False

    def check_if_increment_tournament_round_id_needed(self, round_number):
        logging.debug('ChessMainControllers: check_if_increment_tournament_round_id_needed')
        logging.info('ChessMainControllers: check_if_increment_tournament_round_id_needed: ' +
                     f'round_number={round_number}')
        round_id = int(re.findall(r"\d+", round_number)[0])
        if round_id < self.get_tournament_round_id():
            pass

    def get_expected_tournament_round_id(self, all_matches):
        logging.debug('ChessMainControllers: get_expected_tournament_round_id')
        round_id = 1
        retval = 1
        if len(all_matches) > self.get_nb_matches_per_round():
            retval = float(len(all_matches)) / float(self.get_nb_matches_per_round())
            logging.info(f'ChessMainControllers: get_expected_tournament_round_id(1): ratio={retval} ' +
                         f'nb_m_p_r={self.get_nb_matches_per_round()} len_all_matches{len(all_matches)}')
            decimal = retval - int(retval)
            logging.info(f'ChessMainControllers: get_expected_tournament_round_id(1): {int(retval)} ' +
                         f'{decimal}')
            round_id = int(retval) + 1
            logging.info(f'ChessMainControllers: get_expected_tournament_round_id(1): round_id={round_id}')
            self.set_tournament_round_id(round_id)
        elif all_matches and (len(all_matches) == self.get_nb_matches_per_round()):
            logging.info('ChessMainControllers: get_expected_tournament_round_id(2): ' +
                         f'all_matches={all_matches}')
            logging.info('ChessMainControllers: get_expected_tournament_round_id(2): ' +
                         f'nb_matches_per_round={self.get_nb_matches_per_round()}')
            round_id = self.increment_tournament_round_id()
            logging.info(f'ChessMainControllers: get_expected_tournament_round_id(2): round_id={round_id}')
        else:
            round_id = self.get_tournament_round_id()
            round_id = self.set_tournament_round_id(round_id)
            logging.info(f'ChessMainControllers: get_expected_tournament_round_id(3): round_id={round_id}')
        return round_id

    def is_a_round_terminated(self):
        return self.is_last_round_nb_matches_reached()

    def is_tournament_terminated(self):
        logging.debug('ChessMainControllers: is_tournament_terminated')
        if self.is_last_round_reached_and_end_time_stamped():
            logging.info('ChessMainControllers: is_tournament_terminated: True')
            return True
        else:
            logging.info('ChessMainControllers: is_tournament_terminated: False')
            return False

    def couple_already_has_played(self, first_player, second_player):
        logging.debug('ChessMainControllers: couple_already_has_played')
        logging.info('ChessMainControllers: couple_already_has_played: ' +
                     f'selected_rounds_list={self.selected_rounds_list}')
        if self.selected_rounds_list:
            logging.info(f'ChessMainControllers: couple_already_has_played: first_player={first_player}')
            logging.info(f'ChessMainControllers: couple_already_has_played: second_player={second_player}')
            for a_round in self.selected_rounds_list:
                for a_match in a_round[3]:
                    a_first_player = a_match[0][0]
                    a_second_player = a_match[1][0]
                    if (first_player == a_first_player) and (second_player == a_second_player):
                        a_match = [first_player, second_player]
                        logging.info(f'ChessMainModels: couple_already_has_played: SKIP =====> {a_match}')
                        return True
            logging.info('ChessMainControllers: couple_already_has_played: NOT ALREADY PLAYED =====> ' +
                         f'first_player={first_player} second_player={second_player}')
            return False
        return False

    def get_rounds_and_players_couple_list(self, score_to_update=False):
        logging.debug('ChessMainControllers: get_rounds_and_players_couple_list')
        self.selected_rounds_list, self.selected_players_list = self.get_rounds_and_players()
        logging.info('ChessMainControllers: get_rounds_and_players_couple_list: selected_rounds_list=' +
                     f'{self.selected_rounds_list}')
        logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                     f'players_list={self.selected_players_list}')
        tournament = self.get_selected_tournament()
        if tournament is None:
            return [], []
        # elif (len(self.selected_rounds_list) == self.get_max_rounds_number()) and \
        #      (len(self.selected_rounds_list[-1]) == self.get_nb_matches_per_round):
        #     return self.selected_rounds_list, self.players_couple_list
        tournament_id = tournament[6]
        round_id = self.get_tournament_round_id()
        logging.info(f'ChessMainControllers: get_rounds_and_players_couple_list: tournament_id={tournament_id} ' +
                     f'round_id={round_id} score_to_update={score_to_update}')
        logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                     f'players_list = {self.selected_players_list}')
        logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                     f'players_score = {str(self.players_score)}')
        if self.selected_players_list:
            if score_to_update:
                for current in range(len(self.selected_players_list)):
                    self.selected_players_list[current][4] = \
                        self.players_score.get_score(self.selected_players_list[current][0])
                logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                             f'before sort: players_list = {self.selected_players_list}')
                self.selected_players_list = sorted(self.selected_players_list,
                                                    key=lambda x: float(x[4]), reverse=True)
                logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                             f'after sort:  players_list = {self.selected_players_list}')
                for player in self.selected_players_list:
                    logging.info(f'ChessMainControllers: get_rounds_and_players_couple_list: player={player}')

                self.players_couple_list = self.algorithm_swiss(self.selected_players_list)
            else:
                logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                             f'players_list = {self.selected_players_list}')
                logging.info('ChessMainControllers: get_rounds_and_players_couple_list:' +
                             f'selected_rounds_list={self.selected_rounds_list}')
                nb_players_couple = int(len(self.selected_players_list) / 2)
                self.players_couple_list = []

                for current in range(nb_players_couple):
                    opponent = current + nb_players_couple

                    first_player = [self.selected_players_list[current][0], self.selected_players_list[current][5], 0]
                    second_player = [self.selected_players_list[opponent][0],
                                     self.selected_players_list[opponent][5], 0]

                    logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                                 f'first_player = {first_player}')
                    logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                                 f'second_player = {second_player}')
                    if not self.couple_already_has_played(first_player[0], second_player[0]):
                        self.players_couple_list.append(first_player)
                        self.players_couple_list.append(second_player)
                        # self.all_matches.append([first_player, second_player])

        logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                     f'self.all_matches={self.all_matches}')
        logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                     f'players couples={self.players_couple_list}')
        logging.info('ChessMainControllers: get_rounds_and_players_couple_list: ' +
                     f'self.selected_rounds_list={self.selected_rounds_list}')

        return self.selected_rounds_list, self.players_couple_list, self.selected_players_list

    def reinitialize(self):
        self.rebuild_all_matches()
        self.players_score = ChessPlayersScore()
        self.set_selected_tournament(None)

    def get_matches(self):
        return self.matches

    def rebuild_all_matches(self):
        logging.debug('ChessMainControllers: rebuild_all_matches')
        rounds_list, players_list = self.get_rounds_and_players()
        logging.info(f'ChessMainControllers: rebuild_all_matches (1): rounds_list={rounds_list}')
        new_couples_list = []
        if rounds_list:
            for a_round in rounds_list:
                couples_list = a_round[3]
                for a_couple in couples_list:
                    first_player = a_couple[0]
                    second_player = a_couple[1]
                    first_player[2] = float(first_player[2])
                    second_player[2] = float(second_player[2])
                    new_couples_list.append(a_couple)
                self.all_matches = new_couples_list

        logging.info(f'ChessMainControllers: rebuild_all_matches (2): rounds_list={rounds_list}')
        logging.info(f'ChessMainControllers: rebuild_all_matches: players_list={players_list}')
        logging.info(f'ChessMainControllers: rebuild_all_matches: self.all_matches={self.all_matches}')

        return self.all_matches

    def make_simplified_index_couple_list(self):
        logging.debug('ChessMainControllers: make_simplified_index_couple_list')
        logging.info(f'ChessMainControllers: make_simplified_index_couple_list:  self.all_matches={ self.all_matches}')
        players_couple_list = self.all_matches.copy()
        simplified_index_couple_list = []
        for couple_list in players_couple_list:
            logging.info(f'ChessMainControllers: make_simplified_index_couple_list: couple_list={couple_list}')
            first_player_id = couple_list[0][1]
            second_player_id = couple_list[1][1]
            simplified_index_couple_list.append([first_player_id, second_player_id])
        logging.info('ChessMainControllers: make_simplified_index_couple_list: ' +
                     f'simplified_players_couple_list={simplified_index_couple_list}')
        return simplified_index_couple_list

    def algorithm_swiss(self, players_list):
        logging.debug('ChessMainControllers: algorithm_swiss')
        logging.info(f'ChessMainControllers: algorithm_swiss: players_list={players_list}')
        simplified_index_couple_list = self.make_simplified_index_couple_list()
        logging.info('ChessMainControllers: algorithm_swiss: ' +
                     f'simplified_index_couple_list={simplified_index_couple_list}')
        nb_players_couple = int(len(players_list) / 2)
        new_players_list = []
        opponents_index_list = [i + nb_players_couple for i in range(nb_players_couple)]
        logging.info(f'ChessMainControllers: algorithm_swiss: opponents_index_list={opponents_index_list}')
        i = 0
        for current_index in range(nb_players_couple):
            nb_search_failure = 0
            while nb_search_failure != nb_players_couple:
                opponent_index = opponents_index_list[i]
                logging.info(f'ChessMainControllers: algorithm_swiss: current_idx={current_index}')
                logging.info(f'ChessMainControllers: algorithm_swiss: opponent_idx={opponent_index}')
                if ([players_list[current_index][5], players_list[opponent_index][5]] in
                   simplified_index_couple_list) or \
                   ([players_list[current_index][5], players_list[opponent_index][5]] in
                   simplified_index_couple_list):
                    logging.info('ChessMainControllers: algorithm_swiss: ======================')
                    logging.info(f'ChessMainControllers: algorithm_swiss: {players_list[current_index][5]}')
                    logging.info(f'ChessMainControllers: algorithm_swiss: {players_list[opponent_index][5]}')
                    logging.info('ChessMainControllers: algorithm_swiss: ====== DISCARDED ======')
                    i = (i + 1) % nb_players_couple
                    nb_search_failure += 1
                    continue
                else:
                    logging.info('ChessMainControllers: algorithm_swiss: ====================')
                    logging.info(f'ChessMainControllers: algorithm_swiss: {current_index}')
                    logging.info(f'ChessMainControllers: algorithm_swiss: {opponent_index}')
                    logging.info('ChessMainControllers: algorithm_swiss: ====== FOUND  ======')

                    first_player = [players_list[current_index][0], players_list[current_index][5],
                                    players_list[current_index][4]]
                    second_player = [players_list[opponent_index][0], players_list[opponent_index][5],
                                     players_list[opponent_index][4]]
                    new_players_list.append(first_player)
                    new_players_list.append(second_player)

                    logging.info(f'ChessMainControllers: swiss: current_player={players_list[current_index]}')
                    logging.info(f'ChessMainControllers: swiss: opponent_player={players_list[opponent_index]}')
                    i = (i + 1) % nb_players_couple
                    break
            if nb_search_failure == nb_players_couple:
                continue
        return new_players_list

    def all_matches_append(self, a_player_couple):
        logging.debug('ChessMainControllers: all_matches_append')
        logging.info(f'ChessMainControllers: all_matches_append: before self.all_matches={self.all_matches}')
        logging.info(f'ChessMainControllers: all_matches_append: a_player_couple={a_player_couple}')
        self.all_matches.append(a_player_couple)
        logging.info(f'ChessMainControllers: all_matches_append: after self.all_matches={self.all_matches}')

    def set_player_id(self, player_id):
        self.player_id = player_id
        return self.player_id

    def get_player_id(self):
        self.player_id += 1
        return self.player_id

    def get_tournament_players_ordered_by_name(self):
        rounds_list, players_list = self.get_rounds_and_players()
        ordered_players_list = sorted(players_list, key=itemgetter(0))
        return ordered_players_list

    def get_tournament_players_ordered_by_rank(self):
        rounds_list, players_list = self.get_rounds_and_players()
        ordered_players_list = sorted(players_list, key=itemgetter(4), reverse=True)
        return ordered_players_list

    def get_all_tournaments(self):
        tournaments_list = self.load_tournaments_list()
        return tournaments_list

    def get_a_tournament_rounds(self):
        logging.debug('ChessMainControllers: get_a_tournament_rounds')
        rounds_list, players_list = self.get_rounds_and_players()
        return rounds_list

    def get_a_tournament_matches(self):
        players_list, matches_list = self.get_players_and_matches()
        return players_list, matches_list

    def get_participants_score(self):
        tournament = self.get_selected_tournament()
        players_score = self.my_model.get_participants_score(tournament)
        # final_scores = {}
        # for key, value in players_score.items():
        #     final_scores[key] = value
        # final_scores = sorted(final_scores, key=itemgetter(1), reverse=True)
        # return final_scores
        return players_score

    def get_partial_participant_score_as_sorted_list(self):
        logging.debug('ChessMainControllers: get_partial_participant_score_as_sorted_list')
        players_score = self.players_score.get()
        final_scores = []
        for key, value in players_score.items():
            final_scores.append([key, value])
        final_scores = sorted(final_scores, key=itemgetter(1), reverse=True)
        logging.info(f'ChessMainControllers: get_partial_participant_score_as_sorted_list:final_scores={final_scores}')
        return final_scores

    def get_participant_score_as_sorted_list(self):
        tournament = self.get_selected_tournament()
        players_score = self.my_model.get_participants_score(tournament)
        final_scores = []
        for key, value in players_score.items():
            final_scores.append([key, value])
        final_scores = sorted(final_scores, key=itemgetter(1), reverse=True)
        return final_scores

    def retrieve_participants_score(self):
        tournament = self.get_selected_tournament()
        players_score = self.my_model.get_participants_score(tournament)
        return players_score

    @staticmethod
    def read_controllers_section_config_file():
        logging.debug('ChessMainControllers: read_views_section_config_file')
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
                              ('Lloris', 'Hugo', '07/02/1997', 'Male', 3000, self.get_player_id()),
                              ('Weir', 'Caroline', '07/02/2000', 'Female', 1000, self.get_player_id()),
                              ('Bouhaddi', 'Sarah', '07/02/1986', 'Female', 5000, self.get_player_id())]

        self.save_players_list(dummy_players_list)
        return dummy_players_list

    def save_players_list(self, players_list):
        model_players_list = []
        for player in players_list:
            model_player = ChessMainModels.Player(player[0], player[1], player[2], player[3], player[4], player[5])
            model_players_list.append(model_player)
        status = self.my_model.insert_players_in_db(model_players_list)
        return status

    def save_a_player(self, player):
        model_player = ChessMainModels.Player(player[0], player[1], player[2], player[3], player[4], player[5])
        status = self.my_model.insert_a_player_in_db(model_player)
        return status

    def update_a_player_rank(self, player, new_rank):
        logging.debug(f'update_a_player_rank: new_rank={new_rank}')
        model_player = ChessMainModels.Player(player[0], player[1], player[2], player[3], player[4], player[5])
        status = self.my_model.update_a_player_rank_in_db(model_player)
        return status

    def load_players_list(self):
        logging.debug('ChessMainControllers: load_players_list')
        model_players_list = self.my_model.load_players_in_db()
        players_list = []
        for model_player in model_players_list:
            players_list.append(model_player.unserialize())
        return players_list

    def get_nb_players(self):
        logging.debug('ChessMainControllers: load_players_list')
        model_players_list = self.my_model.load_players_in_db()
        return len(model_players_list)

    def get_players_ordered_by_name(self):
        players_list = self.load_players_list()
        ordered_players_list = sorted(players_list, key=itemgetter(0))
        return ordered_players_list

    def get_players_ordered_by_rank(self):
        players_list = self.load_players_list()
        ordered_players_list = sorted(players_list, key=itemgetter(4), reverse=True)
        return ordered_players_list

    def get_dummy_tournaments_list(self):
        dummy_tournaments_list = [('Toronto tournament', 'Toronto', '07/03/1984', 4, 'Blitz', 'Bitz tournament',
                                   self.get_tournament_id(), [], []),
                                  ('Paris tournament', 'Paris', '07/03/1984', 3, 'Bullet', 'Bullet tournament',
                                   self.get_tournament_id(), [], []),
                                  ('Milan tournament', 'Milan', '07/03/1984', 2, 'Fast', 'Fast tournament',
                                   self.get_tournament_id(), [], [])]

        self.save_tournaments_list(dummy_tournaments_list)
        return dummy_tournaments_list

    def save_tournaments_list(self, tournaments_list):
        model_tournaments_list = []
        for tournament in tournaments_list:
            model_tournament = ChessMainModels.Tournament(tournament[0], tournament[1], tournament[2], tournament[3],

                                                          tournament[4], tournament[5], tournament[6], tournament[7],
                                                          tournament[8], participants_score=dict())
            model_tournaments_list.append(model_tournament)
        status = self.my_model.insert_tournaments_in_db(model_tournaments_list)
        return status

    def save_a_tournament(self, tournament):
        model_tournament = ChessMainModels.Tournament(tournament[0], tournament[1], tournament[2], tournament[3],
                                                      tournament[4], tournament[5], tournament[6], [],
                                                      [], participants_score=dict())
        status = self.my_model.insert_a_tournament_in_db(model_tournament)
        return status

    def load_tournaments_list(self):
        logging.debug('ChessMainControllers: load_tournaments_list')
        model_tournaments_list = self.my_model.load_tournaments_in_db()
        tournaments_list = []

        self.selected_players_list = []
        self.selected_rounds_list = []
        self.players_couple_list = []
        self.all_matches = []
        self.players_score = ChessPlayersScore()
        self.matches = ChessMatches()

        for model_tournament in model_tournaments_list:
            round_id = 1
            a_tournament = model_tournament.unserialize()
            tournaments_list.append(a_tournament)
            logging.info(f'ChessMainControllers: load_tournaments_list: model_tournament = {model_tournament}')
            logging.info(f'ChessMainControllers: load_tournaments_list: rounds = {tournaments_list}')

            logging.info(f'ChessMainControllers: load_tournaments_list: a_tournament = {a_tournament}')
            tournament_id = a_tournament[6]
            matches = a_tournament[8]
            logging.info(f'ChessMainControllers: load_tournaments_list: tournament_id = {tournament_id}')
            logging.info(f'ChessMainControllers: load_tournaments_list: matches={matches}')
            self.matches.set(tournament_id, matches)
            if not matches:
                logging.info('ChessMainControllers: load_tournaments_list: initialize_tournament_round_id ' +
                             f'tournament_id={tournament_id} round_id={round_id}')
                self.initialize_tournament_round_id(tournament_id, round_id)
            else:
                round_id = int(re.findall(r"\d+", matches[-1][0])[0])
                logging.info('ChessMainControllers: load_tournaments_list: initialize_tournament_round_id ' +
                             f'tournament_id={tournament_id} round_id={round_id}')
                self.initialize_tournament_round_id(tournament_id, round_id)

            self.players_score.set(self.my_model.get_participants_score(a_tournament))
        return tournaments_list

    def set_tournament_id(self, tournament_id):
        self.tournament_id = tournament_id
        return self.tournament_id

    def get_tournament_id(self):
        self.tournament_id += 1
        return self.tournament_id
