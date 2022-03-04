import json
import logging
from tinydb import TinyDB, Query

PLAYERS_DB = 'c:/temp/P4/players_db.json'
TOURNAMENTS_DB = 'c:/temp/P4/tournaments_db.json'


class VirtualModel:
    def __init__(self):
        pass

    def run(self):
        pass

class Player:
    def __init__(self,
                 last_name=None,
                 first_name=None,
                 birthdate=None,
                 gender=None,
                 rank=None,
                 player_id=0
                 ):
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.player_id = player_id

    def serialized(self):
        player_infos = {}
        player_infos['Nom'] = self.last_name
        player_infos['Prenom'] = self.first_name
        player_infos['Date de naissance'] = self.birthdate
        player_infos['Sexe'] = self.gender
        player_infos['Classement'] = self.ranking
        player_infos['Score'] = self.tournament_score
        player_infos['Id du joueur'] = self.player_id
        return player_infos

    def unserialized(self, serialized_player):
        last_name = serialized_player["Nom"]
        first_name = serialized_player["Prenom"]
        birthdate = serialized_player["Date de naissance"]
        gender = serialized_player["Sexe"]
        ranking = serialized_player["Classement"]
        tournament_score = serialized_player["Score"]
        player_id = serialized_player["Id du joueur"]
        return Player(last_name,
                      first_name,
                      birthdate,
                      gender,
                      ranking,
                      tournament_score,
                      player_id
                      )

class ChessMainModel(VirtualModel):
    def __init__(self):
        super().__init__()
        self.my_controller = None
        players_db = TinyDB(PLAYERS_DB)
        self.players_table = players_db.table('players')
        tournaments_db = TinyDB(TOURNAMENTS_DB)
        self.tournaments_table = tournaments_db.table('tournaments')

    def set_my_controller(self, controller):
        self.my_controller = controller

    def is_players_validate(self, players_list):
        return True

    def check_and_insert_players_in_db(self, players_list):
        if self.is_players_validate(players_list):
            self.players_table.truncate()
            for player in players_list:
                logging.info(f'{player}')
                player_entry = self.serialize_player(player)
                self.players_table.insert(player_entry)
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
        player_entry = {}
        player_entry['LastName'] = player[0]
        player_entry['FirstName'] = player[1]
        player_entry['Birthdate'] = player[2]
        player_entry['Gender'] = player[3]
        player_entry['Rank'] = player[4]

        logging.info(f'{player_entry}')
        return player_entry

    def unserialize_player(self, player_entry):
        last_name = player_entry["LastName"]
        first_name = player_entry["FirstName"]
        birthdate = player_entry["Birthdate"]
        gender = player_entry["Gender"]
        rank = player_entry["Rank"]
        player = [last_name, first_name, birthdate, gender, rank]
        return player
