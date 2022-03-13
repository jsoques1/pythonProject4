import json
import configparser
import logging
from tinydb import TinyDB, where, Query



class VirtualModel:
    def __init__(self):
        pass

    def run(self):
        pass


class Tournament:
    def __init__(self, name=None, location=None, date=None, tournament_rounds_number=None, time_control=None,
                 description=None, tournament_id=0, players=[], rounds=[], players_score=[]):
        self.name = name
        self.location = location
        self.date = date
        self.rounds_number = tournament_rounds_number
        self.time_control = time_control
        self.description = description
        self.tournament_id = tournament_id
        self.players = players
        self.rounds = rounds
        self.players_score = players_score

    def serialize(self):
        tournament_entry = dict()
        tournament_entry['Name'] = self.name
        tournament_entry['Location'] = self.location
        tournament_entry['Date'] = self.date
        tournament_entry['RoundsNumber'] = self.rounds_number
        tournament_entry['TimeControl'] = self.time_control
        tournament_entry['Description'] = self.description
        tournament_entry['TournamentId'] = self.tournament_id
        tournament_entry['Players'] = self.players
        tournament_entry['Rounds'] = self.rounds
        tournament_entry['PlayersScore'] = self.players_score
        return tournament_entry

    def unserialize(self):
        retval = (self.name, self.location, self.date, self.rounds_number, self.time_control, self.description,
                  self.tournament_id, self.players, self.rounds, self.players_score)
        return retval

    def __str__(self):
        return f'{self.name} {self.location} {self.date} {self.rounds_number} {self.time_control} {self.description} \
{self.tournament_id} {self.players} {self.rounds} {self.players_score}'

    
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
        retval = (self.last_name, self.first_name, self.birthdate, self.gender, self.rank, self.player_id)
        return retval

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.birthdate} {self.gender} {self.rank} {self.player_id}'


class Round:
    def __init__(self, rounds_number=1, start_time=None, end_time=None, match_list=None):
        self.rounds_number = rounds_number
        self.start_time = start_time
        self.end_time = end_time
        self.match_list = match_list

    def serialize(self):
        round_entry = dict()
        round_entry['RoundsNumber'] = self.rounds_number
        round_entry['StartTime'] = self.start_time
        round_entry['EndTime'] = self.end_time
        round_entry['MatchList'] = self.match_list
        return round_entry

    def unserialize(self):
        retval = (self.rounds_number, self.start_time, self.end_time, self.match_list)
        return retval

    def __repr__(self):
        return f"{self.start_time} {self.end_time} {self.match_list}"
    
    
class Match:
    def __init__(self, first_player=None, second_player=None, first_player_score=0, second_player_score=0, match_id=0):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_score = first_player_score
        self.second_player_score = second_player_score
        self.match_id = match_id

    def serialize(self):
        match_entry = dict()
        match_entry['first_player'] = self.first_player
        match_entry['second_player'] = self.second_player
        match_entry['first_player_score'] = self.first_player_score
        match_entry['second_player_score'] = self.second_player_score
        match_entry['match_id'] = self.match_id
        return match_entry

    def unserialize(self):
        retval = (self.first_player, self.second_player, self.first_player_score,
                  self.second_player_score, self.match_id)
        return retval

    def __str__(self):
        return f"{self.match_id} {self.first_player} {self.second_player} {self.first_player_score} \
    {self.second_player_score} {self.match_id}"


class ChessMainModel(VirtualModel):
    def __init__(self):
        super().__init__()

        self.my_controller = None
        db_dir, players_db, tournaments_db = ChessMainModel.read_models_section_config_file()
        self.players_db = TinyDB(db_dir + '/' + players_db)
        self.players_db.default_table_name = 'Players'
        self.tournaments_db = TinyDB(db_dir + '/' + tournaments_db)
        self.tournaments_db.default_table_name = 'Tournaments'

    @staticmethod
    def read_models_section_config_file():
        logging.debug('ChessMainModels : read_models_section_config_file')
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
            self.players_db.truncate()
            for player in players_list:
                player_entry = self.serialize_player(player)
                self.players_db.insert(player_entry)
            return True
        else:
            return False

    def check_and_insert_a_player_in_db(self, player):
        if self.is_players_validate([player]):
            player_entry = self.serialize_player(player)
            self.players_db.insert(player_entry)
            return True
        else:
            return False

    def check_and_udate_a_player_rank_in_db(self, player):
        if self.is_players_validate([player]):
            print(f'update Rank = {player.rank} where PlayerdId == {player.player_id}')
            retval = self.players_db.update({"Rank": int(player.rank)}, doc_ids=[int(player.player_id)])
            print(retval)
            return True
        else:
            return False

    def load_players_in_db(self):
        logging.debug('ChessMainModels : load_players_in_db')
        players_list = []
        for player_entry in self.players_db.all():
            players_list.append(self.unserialize_player(player_entry))
        return players_list

    def serialize_player(self, player):
        player_entry = player.serialize()
        logging.info(f'ChessMainModels : player_entry={player_entry}')
        return player_entry

    def unserialize_player(self, player_entry):
        player = Player(player_entry["LastName"],
                        player_entry["FirstName"],
                        player_entry["Birthdate"],
                        player_entry["Gender"],
                        player_entry["Rank"],
                        player_entry["PlayerId"])
        logging.info(f'ChessMainModels : player={str(player)}')
        return player

    def is_tournaments_validate(self, tournaments_list):
        return True

    def check_and_insert_tournaments_in_db(self, tournaments_list):
        if self.is_tournaments_validate(tournaments_list):
            self.tournaments_db.truncate()
            for tournament in tournaments_list:
                tournament_entry = self.serialize_tournament(tournament)
                self.tournaments_db.insert(tournament_entry)
            return True
        else:
            return False

    def check_and_insert_a_tournament_in_db(self, tournament):
        if self.is_tournaments_validate([tournament]):
            tournament_entry = self.serialize_tournament(tournament)
            self.tournaments_db.insert(tournament_entry)
            return True
        else:
            return False

    def update_a_tournament_players_list(self, tournament, players_list):
        logging.debug('ChessMainModels : update_a_tournament_players_list')
        logging.info(f'ChessMainModels : players_list = {players_list}')
        retval = self.tournaments_db.update({"Players": players_list}, doc_ids=[int(tournament[6])])
        print(retval)

    def get_tournament_rounds_players_list(self, tournament):
        logging.debug('ChessMainModels : get_tournament_rounds_players_list')
        logging.info(f'ChessMainModels : selected_tournament = {tournament}')
        tournament_entry = self.tournaments_db.get(doc_id=int(tournament[6]))
        logging.info(f'ChessMainModels : rounds = {tournament_entry["Rounds"]}')
        logging.info(f'ChessMainModels : players = {tournament_entry["Players"]}')
        return tournament_entry['Rounds'], tournament_entry['Players']

    def update_a_tournament_round(self, tournament, round_id, round_start_time, round_end_time, match_list, players_score):
        logging.debug('ChessMainModels : update_a_tournament_rounds')
        logging.info(f'ChessMainModels : selected_tournament = {tournament}')
        tournament_entry = self.tournaments_db.get(doc_id=int(tournament[6]))
        rounds_list = tournament_entry['Rounds']
        rounds_list.append([round_id, round_start_time, round_end_time, match_list])
        retval1 = self.tournaments_db.update({"Rounds": rounds_list}, doc_ids=[int(tournament[6])])
        retval2 = self.tournaments_db.update({"PlayersScore": players_score}, doc_ids=[int(tournament[6])])
        return retval1 and retval2

    def get_players_score(self, tournament):
        logging.debug('ChessMainModels : get_players_score')
        logging.info(f'ChessMainModels : selected_tournament = {tournament}')
        tournament_entry = self.tournaments_db.get(doc_id=int(tournament[6]))
        retval = tournament_entry['PlayersScore']
        return retval

    def get_tournament_rounds_list(self, tournament):
        logging.debug('ChessMainModels : get_tournament_rounds_list')
        logging.info(f'ChessMainModels : selected_tournament = {tournament}')
        tournament_entry = self.tournaments_db.get(doc_id=int(tournament[6]))
        retval = tournament_entry['Rounds']
        return retval

    def load_tournaments_in_db(self):
        logging.debug('ChessMainModels : load_tournaments_in_db')
        tournaments_list = []
        for tournament_entry in self.tournaments_db.all():
            tournaments_list.append(self.unserialize_tournament(tournament_entry))
            logging.info(f'ChessMainModels : Rounds = {tournament_entry["Rounds"]}')
        return tournaments_list

    def serialize_tournament(self, tournament):
        tournament_entry = tournament.serialize()
        logging.info(f'ChessMainModels : tournament_entry={tournament_entry}')
        return tournament_entry

    def unserialize_tournament(self, tournament_entry):
        logging.debug('unserialize_tournament')
        tournament = Tournament(tournament_entry["Name"],
                                tournament_entry["Location"],
                                tournament_entry["Date"],
                                tournament_entry["RoundsNumber"],
                                tournament_entry["TimeControl"],
                                tournament_entry["Description"],
                                tournament_entry["TournamentId"],
                                tournament_entry["Players"],
                                tournament_entry["Rounds"],
                                tournament_entry['PlayersScore'])
        logging.info(f'ChessMainModels : tournament={str(tournament)}')
        return tournament
    
    def unserialize_round(self, round_entry):
        tournament_rounds_number = Round(round_entry['RoundsNumber'],
                                 round_entry['StartTime'],
                                 round_entry['EndTime'],
                                 round_entry['MatchList'])
        retval = (f'tournament={str(tournament_rounds_number)}')
        return retval