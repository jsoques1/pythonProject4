import json
import configparser
import logging
from tinydb import TinyDB, where, Query



class VirtualModel:
    def __init__(self):
        pass

    def run(self):
        pass

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

