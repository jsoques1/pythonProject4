import json
import configparser
import logging
from tinydb import TinyDB, where, Query



class VirtualModel:
    def __init__(self):
        pass

    def run(self):
        pass

class Round:
    def __init__(self, start_time=None, end_time=None, match_list=None):
        self.start_time = start_time
        self.end_time = end_time
        self.match_list = []
        self.round_list = []

    # def serialized(self):
    #     tour_infos = {}
    #     tour_infos['Nom'] = self.name
    #     tour_infos['Debut'] = self.begin_time
    #     tour_infos['Fin'] = self.end_time
    #     tour_infos['Matchs'] = self.list_of_finished_matchs
    #     return tour_infos
    #
    # def unserialized(self, serialized_tour):
    #     name = serialized_tour['Nom']
    #     begin_time = serialized_tour['Debut']
    #     end_time = serialized_tour['Fin']
    #     list_of_finished_matchs = serialized_tour['Matchs']
    #     return Tour(name,
    #                 begin_time,
    #                 end_time,
    #                 list_of_finished_matchs
    #                 )
    #
    # def __repr__(self):
    #     return f"{self.name} - Début : {self.begin_time}. Fin : {self.end_time}."
    #
    # def run(self, sorted_players_list, tournament_object):
    #     self.view = view_main.TourDisplay()
    #     self.list_of_tours = []
    #     self.list_of_finished_matchs = []
    #     self.name = "Tour " + str(len(tournament_object.list_of_tours) + 1)
    #     # Tour.TOUR_NUMBER += 1
    #
    #     self.begin_time, self.end_time = self.view.display_tournament_time()
    #
    #     # tant qu'il y a des joueurs dans la liste, ajoute des instances de 'match' dans la liste 'list_of_tours'
    #     while len(sorted_players_list) > 0:
    #         match_instance = Match(self.name, sorted_players_list[0], sorted_players_list[1])
    #         Match.MATCH_NUMBER += 1
    #         self.list_of_tours.append(match_instance)
    #         del sorted_players_list[0:2]
    #
    #     self.view.display_tour(self.name, self.list_of_tours)
    #
    #     for match in self.list_of_tours:
    #
    #         valid_score_player_1 = False
    #         while not valid_score_player_1:
    #             try:
    #                 score_player_1 = input(f"Entrez le score de {match.player_1} :")
    #                 float(score_player_1)
    #             except Exception:
    #                 print("Vous devez entrer 0, 0.5, ou 1")
    #             else:
    #                 match.score_player_1 = float(score_player_1)
    #                 match.player_1.tournament_score += float(score_player_1)
    #                 valid_score_player_1 = True
    #
    #         valid_score_player_2 = False
    #         while not valid_score_player_2:
    #             try:
    #                 score_player_2 = input(f"Entrez le score de {match.player_2} :")
    #                 float(score_player_2)
    #             except Exception:
    #                 print("Vous devez entrer 0, 0.5, ou 1")
    #             else:
    #                 match.score_player_2 = float(score_player_2)
    #                 match.player_2.tournament_score += float(score_player_2)
    #                 valid_score_player_2 = True
    #
    #         self.list_of_finished_matchs.append(([match.player_1.player_id, match.score_player_1],
    #                                              [match.player_2.player_id, match.score_player_2]))
    #
    #     return Tour(self.name, self.begin_time, self.end_time, self.list_of_finished_matchs)


class Match:
    def __init__(self, first_player=None, second_player=None, first_player_score=0, second_player_score=0, match_id=0):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_score = first_player_score
        self.second_player_score = second_player_score
        self.match_id = match_id

    def __str__(self):
        return f"{self.match_id} {self.first_player} {self.second_player}"


class Tournament:
    def __init__(self, name=None, location=None, date=None, tournament_round=None, time_control=None, description=None, tournament_id=0):
        self.name = name
        self.location = location
        self.date = date
        self.round = tournament_round
        self.time_control = time_control
        self.description = description
        self.tournament_id = tournament_id

    def serialize(self):
        tournament_entry = dict()
        tournament_entry['Name'] = self.name
        tournament_entry['Location'] = self.location
        tournament_entry['Date'] = self.date
        tournament_entry['Round'] = self.round
        tournament_entry['TimeControl'] = self.time_control
        tournament_entry['Description'] = self.description
        tournament_entry['TournamentId'] = self.tournament_id
        tournament_entry['Players'] = []
        tournament_entry['Rounds'] = []
        return tournament_entry

    def unserialize(self):
        return (self.name, self.location, self.date, self.round, self.time_control, self.description, self.tournament_id)

    def __str__(self):
        return f'{self.name} {self.location} {self.date} {self.round} {self.time_control} {self.description} {self.tournament_id}'
    
class Player:
    def __init__(self, last_name=None, first_name=None, birthdate=None, gender=None, rank=None, player_id=0):
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.player_id = player_id

    def serialize(self):
        player_entry = dict()
        player_entry['LastName'] = self.last_name
        player_entry['FirstName'] = self.first_name
        player_entry['Birthdate'] = self.birthdate
        player_entry['Gender'] = self.gender
        player_entry['Rank'] = self.rank
        player_entry['PlayerId'] = self.player_id
        return player_entry

    def unserialize(self):
        return (self.last_name, self.first_name, self.birthdate, self.gender, self.rank, self.player_id)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.birthdate} {self.gender} {self.rank} {self.player_id}'


class ChessMainModel(VirtualModel):
    def __init__(self):
        super().__init__()

        self.my_controller = None
        db_dir, players_db, tournaments_db = ChessMainModel.read_models_section_config_file()
        players_db = TinyDB(db_dir + '/' + players_db)
        self.players_table = players_db.table('Players')
        tournaments_db = TinyDB(db_dir + '/' + tournaments_db)
        self.tournaments_table = tournaments_db.table('Tournaments')

    @staticmethod
    def read_models_section_config_file():
        logging.debug('read_models_section_config_file')
        config = configparser.ConfigParser()
        config.read('MyChessApp.ini')
        db_dir = config['models']['db_dir']
        players_db = config['models']['players_db']
        tournaments_db = config['models']['tournaments_db']
        return db_dir, players_db, tournaments_db

    def set_my_controller(self, controller):
        self.my_controller = controller

    def is_players_validate(self, players_list):
        return True

    def check_and_insert_players_in_db(self, players_list):
        if self.is_players_validate(players_list):
            self.players_table.truncate()
            for player in players_list:
                player_entry = self.serialize_player(player)
                self.players_table.insert(player_entry)
            return True
        else:
            return False

    def check_and_insert_a_player_in_db(self, player):
        if self.is_players_validate([player]):
            player_entry = self.serialize_player(player)
            self.players_table.insert(player_entry)
            return True
        else:
            return False

    def check_and_udate_a_player_rank_in_db(self, player):
        if self.is_players_validate([player]):
            print(f'update Rank = {player.rank} where PlayerdId == {player.player_id}')
            retval = self.players_table.update({"Rank": int(player.rank)}, doc_ids=[int(player.player_id)])
            print(retval)
            return True
        else:
            return False

    def load_players_in_db(self):
        logging.debug('load_players_in_db')
        players_list = []
        for player_entry in self.players_table.all():
            players_list.append(self.unserialize_player(player_entry))
        return players_list


    def serialize_player(self, player):
        player_entry = player.serialize()
        logging.info(f'player_entry={player_entry}')
        return player_entry


    def unserialize_player(self, player_entry):
        player = Player(player_entry["LastName"],
                        player_entry["FirstName"],
                        player_entry["Birthdate"],
                        player_entry["Gender"],
                        player_entry["Rank"],
                        player_entry["PlayerId"])
        logging.info(f'player={str(player)}')
        return player


    def is_tournaments_validate(self, tournaments_list):
        return True

    def check_and_insert_tournaments_in_db(self, tournaments_list):
        if self.is_tournaments_validate(tournaments_list):
            self.tournaments_table.truncate()
            for tournament in tournaments_list:
                tournament_entry = self.serialize_tournament(tournament)
                self.tournaments_table.insert(tournament_entry)
            return True
        else:
            return False

    def check_and_insert_a_tournament_in_db(self, tournament):
        if self.is_tournaments_validate([tournament]):
            tournament_entry = self.serialize_tournament(tournament)
            self.tournaments_table.insert(tournament_entry)
            return True
        else:
            return False

    def update_a_tournament_players_list(self, tournament, players_list):
        retval = self.tournaments_table.update({"Players": players_list}, doc_ids=[int(tournament[6])])
        print(retval)

    def load_tournaments_in_db(self):
        logging.debug('load_tournaments_in_db')
        tournaments_list = []
        for tournament_entry in self.tournaments_table.all():
            tournaments_list.append(self.unserialize_tournament(tournament_entry))
        return tournaments_list

    def serialize_tournament(self, tournament):
        tournament_entry = tournament.serialize()
        logging.info(f'tournament_entry={tournament_entry}')
        return tournament_entry

    def unserialize_tournament(self, tournament_entry):
        tournament = Tournament(tournament_entry["Name"],
                                tournament_entry["Location"],
                                tournament_entry["Date"],
                                tournament_entry["Round"],
                                tournament_entry["TimeControl"],
                                tournament_entry["Description"],
                                tournament_entry["TournamentId"])
        logging.info(f'tournament={str(tournament)}')
        return tournament