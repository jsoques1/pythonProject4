import logging
from operator import itemgetter
from ChessViews import ChessMainViews
from tkinter import messagebox
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
        self.player_id = 0
        self.tournament_id = 0
        self.selected_players_list = []
        self.selected_tournament = None

    def run(self):
        self.my_view.set_my_controller(self)
        self.my_model.set_my_controller(self)
        self.my_view.display_interface()

    def set_selected_tournament(self, tournament):
        self.selected_tournament = tournament

    def get_selected_tournament(self):
        return self.selected_tournament

    def set_selected_players_list(self, selected_players_list):
        print(selected_players_list)
        self.selected_players_list = selected_players_list

    def get_selected_players_list(self):
        return(self.selected_players_list)

    def assign_selected_players_to_selected_tournament(self):
        logging.debug('assign_selected_players_to_selected_tournament')
        selected_tournament = self.get_selected_tournament()
        selected_players_list = self.get_selected_players_list()
        if selected_tournament is None:
            messagebox.showerror('Error', 'No selected tournament')
        elif selected_players_list == []:
            messagebox.showerror('Error', 'No selected players')
        else:
            messagebox.showinfo('Info', 'Selected players have been assigned to the tournament')
            sorted_selected_players_list = sorted(selected_players_list, key=itemgetter(4), reverse=True)
            logging.info(sorted_selected_players_list)
            self.my_model.update_a_tournament_players_list(selected_tournament, sorted_selected_players_list)


    def set_player_id(self, player_id):
        self.player_id = player_id
        return self.player_id

    def get_player_id(self):
        self.player_id += 1
        return self.player_id

    # @staticmethod
    # def read_controls_section_config_file():
    #     logging.debug('read_models_section_config_file')
    #     config = configparser.ConfigParser()
    #     config.read('MyChessApp.ini')
    #     db_dir = config['controls']['db_dir']
    #     players_db = config['models']['players_db']
    #     tournaments_db = config['models']['tournaments_db']
    #     return db_dir, players_db, tournaments_db
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
        logging.debug('load_players_list')
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

    def load_tournaments_list(self):
        logging.debug('load_tournaments_list')
        model_tournaments_list = self.my_model.load_tournaments_in_db()
        tournaments_list = []
        for model_tournament in model_tournaments_list:
           tournaments_list.append(model_tournament.unserialize())
        return tournaments_list

    def set_tournament_id(self, tournament_id):
        self.tournament_id = tournament_id
        return self.tournament_id

    def get_tournament_id(self):
        self.tournament_id += 1
        return self.tournament_id
