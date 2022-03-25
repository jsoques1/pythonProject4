import configparser
import logging
from tinydb import TinyDB


class VirtualModel:
    def __init__(self):
        pass

    def run(self):
        pass


class Tournament:
    def __init__(self, name=None, location=None, date=None, tournament_rounds_number=None, time_control=None,
                 description=None, tournament_id=0, participants=None, rounds=None, participants_score=None):
        self.name = name
        self.location = location
        self.date = date
        self.rounds_number = tournament_rounds_number
        self.time_control = time_control
        self.description = description
        self.tournament_id = tournament_id
        self.participants = participants
        self.rounds = rounds
        self.participants_score = participants_score

    def serialize(self):
        tournament_entry = dict()
        tournament_entry['Name'] = self.name
        tournament_entry['Location'] = self.location
        tournament_entry['Date'] = self.date
        tournament_entry['RoundsNumber'] = self.rounds_number
        tournament_entry['TimeControl'] = self.time_control
        tournament_entry['Description'] = self.description
        tournament_entry['TournamentId'] = self.tournament_id
        tournament_entry['Participants'] = self.participants
        tournament_entry['Rounds'] = self.rounds
        tournament_entry['ParticipantsScore'] = self.participants_score
        return tournament_entry

    def unserialize(self):
        retval = (self.name, self.location, self.date, self.rounds_number, self.time_control, self.description,
                  self.tournament_id, self.participants, self.rounds, self.participants_score)
        return retval

    def __str__(self):
        return f'{self.name} {self.location} {self.date} {self.rounds_number} {self.time_control} ' + \
               f'{self.description} {self.tournament_id} {self.participants} {self.rounds} {self.participants_score}'


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


class ChessMainModel(VirtualModel):
    def __init__(self):
        super().__init__()

        self.my_controller = None
        db_dir, players_db, tournaments_db = ChessMainModel.read_models_section_config_file()
        self.participants_db = TinyDB(db_dir + '/' + players_db)
        self.participants_db.default_table_name = 'Players'
        self.tournaments_db = TinyDB(db_dir + '/' + tournaments_db)
        self.tournaments_db.default_table_name = 'Tournaments'

    @staticmethod
    def read_models_section_config_file():
        logging.debug('ChessMainModels: read_models_section_config_file')
        config = configparser.ConfigParser()
        config.read('MyChessApp.ini')
        db_dir = config['models']['db_dir']
        players_db = config['models']['players_db']
        tournaments_db = config['models']['tournaments_db']
        return db_dir, players_db, tournaments_db

    def set_my_controller(self, controller):
        self.my_controller = controller

    def insert_players_in_db(self, players_list):
        self.participants_db.truncate()
        for player in players_list:
            player_entry = self.make_a_player_from_entry(player)
            self.participants_db.insert(player_entry)
        return True

    def insert_a_player_in_db(self, player):
        # player_entry = self.make_a_player_from_entry(player)
        self.participants_db.insert(player.serialize())
        return True

    def update_a_player_rank_in_db(self, player):
        self.participants_db.update({"Rank": int(player.rank)}, doc_ids=[int(player.player_id)])
        return True

    def load_players_in_db(self):
        logging.debug('ChessMainModels: load_players_in_db')
        players_list = []
        for player_entry in self.participants_db.all():
            players_list.append(ChessMainModel.make_a_player_from_entry(player_entry))
        return players_list

    @staticmethod
    def make_a_player_entry(player):
        player_entry = player.serialize()
        logging.info(f'ChessMainModels: player_entry={player_entry}')
        return player_entry

    @staticmethod
    def make_a_player_from_entry(player_entry):
        logging.info(f'ChessMainModels: player={player_entry}')
        player = Player(player_entry["LastName"],
                        player_entry["FirstName"],
                        player_entry["Birthdate"],
                        player_entry["Gender"],
                        player_entry["Rank"],
                        player_entry["PlayerId"])
        logging.info(f'ChessMainModels: player={str(player)}')
        return player

    def insert_tournaments_in_db(self, tournaments_list):
        self.tournaments_db.truncate()
        for tournament in tournaments_list:
            tournament_entry = self.make_a_tournament_entry(tournament)
            self.tournaments_db.insert(tournament_entry)
        return True

    def insert_a_tournament_in_db(self, tournament):
        tournament_entry = self.make_a_tournament_entry(tournament)
        self.tournaments_db.insert(tournament_entry)
        return True

    def update_a_tournament_players_list(self, tournament, players_list):
        logging.debug('ChessMainModels: update_a_tournament_players_list')
        logging.info(f'ChessMainModels: players_list = {players_list}')
        retval = self.tournaments_db.update({"Participants": players_list}, doc_ids=[int(tournament[6])])
        return retval

    def get_rounds_and_players_and_score(self, tournament):
        logging.debug('ChessMainModels: get_rounds_and_players_and_score')
        logging.info(f'ChessMainModels: selected_tournament = {tournament}')
        tournament_entry = self.tournaments_db.get(doc_id=int(tournament[6]))
        logging.info(f'ChessMainModels: get_rounds_and_players_and_score: rounds={tournament_entry["Rounds"]}')
        logging.info(f'ChessMainModels: get_rounds_and_players_and_score: {tournament_entry["Participants"]}')
        logging.info(f'ChessMainModels: get_rounds_and_players_and_score: {tournament_entry["ParticipantsScore"]}')
        return tournament_entry['Rounds'], tournament_entry['Participants'], tournament_entry['ParticipantsScore']

    def update_a_tournament_round(self, tournament_id, all_rounds, participants_score):
        logging.debug('ChessMainModels: update_a_tournament_rounds')
        logging.info(f'ChessMainModels: selected_tournament = {tournament_id}')
        retval1 = self.tournaments_db.update({"Rounds": all_rounds}, doc_ids=[int(tournament_id)])
        retval2 = self.tournaments_db.update({"ParticipantsScore": participants_score}, doc_ids=[int(tournament_id)])
        return retval1 and retval2

    def get_participants_score(self, tournament):
        logging.debug('ChessMainModels: get_participants_score')
        logging.info(f'ChessMainModels: selected_tournament = {tournament}')
        tournament_entry = self.tournaments_db.get(doc_id=int(tournament[6]))
        logging.info(f"ChessMainModels: get_participants_score: score = {tournament_entry['ParticipantsScore']}")
        return tournament_entry['ParticipantsScore']

    def get_tournament_rounds_list(self, tournament):
        logging.debug('ChessMainModels: get_tournament_rounds_list')
        logging.info(f'ChessMainModels: selected_tournament = {tournament}')
        tournament_entry = self.tournaments_db.get(doc_id=int(tournament[6]))
        retval = tournament_entry['Rounds']
        return retval

    def load_tournaments_in_db(self):
        logging.debug('ChessMainModels: load_tournaments_in_db')
        tournaments_list = []
        for tournament_entry in self.tournaments_db.all():
            tournaments_list.append(self.make_a_tournament_from_entry(tournament_entry))
            logging.info(f'ChessMainModels: load_tournaments_in_db: Rounds = {tournament_entry["Rounds"]}')
        logging.info(f'ChessMainModels: load_tournaments_in_db: tournaments_list = {tournaments_list}')
        return tournaments_list

    @staticmethod
    def make_a_tournament_entry(tournament):
        tournament_entry = tournament.serialize()
        logging.info(f'ChessMainModels: tournament_entry={tournament_entry}')
        return tournament_entry

    @staticmethod
    def make_a_tournament_from_entry(tournament_entry):
        logging.debug('make_a_tournament_from_entry')
        logging.debug(f'make_a_tournament_from_entry: {tournament_entry}')
        tournament = Tournament(tournament_entry["Name"],
                                tournament_entry["Location"],
                                tournament_entry["Date"],
                                tournament_entry["RoundsNumber"],
                                tournament_entry["TimeControl"],
                                tournament_entry["Description"],
                                tournament_entry["TournamentId"],
                                tournament_entry["Participants"],
                                tournament_entry["Rounds"],
                                tournament_entry['ParticipantsScore'])
        logging.info(f'ChessMainModels: tournament={str(tournament)}')
        return tournament
