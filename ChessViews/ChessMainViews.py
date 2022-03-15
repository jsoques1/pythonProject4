import configparser
import logging
from operator import itemgetter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkcalendar import DateEntry
from ChessUtils import ChessUtils


class ChessBasicView:
    def __init__(self, controller):
        self.my_controller = controller
        self.is_built = False
        self.is_debug = ChessBasicView.read_views_section_config_file()
        self.tree = None
        self.is_already_created = False
        self.main_window = None
        self.tree_frame = None
        self.is_on = False

    def is_visible(self):
        return self.is_on

    def set_visible(self):
        self.is_on = True
        return self.is_on

    def set_not_visible(self):
        self.is_on = False
        return self.is_on

    def set_my_controller(self, controller):
        self.my_controller = controller

    def item_selected(self, event, tree):
        pass

    def sort_tree_column(self, event):
        pass

    def show_all(self):
        pass

    def hide_all(self):
        pass

    def show_actions_frame(self):
        pass

    @staticmethod
    def read_views_section_config_file():
        logging.debug(f'ChessMainViews :  : read_views_section_config_file')
        config = configparser.ConfigParser()
        config.read('MyChessApp.ini')
        is_debug = config['views']['is_debug']
        return is_debug

    def generate_report(self):
        pass

    def activate_debug(self, is_debug):
        pass


"""
    ChessTournamentsView
"""


class ChessTournamentsView(ChessBasicView):
    def __init__(self, controller):
        super().__init__(controller)
        # self.my_controller = controller
        # self.is_built = False
        # self.is_debug = None

        self.action_frame = None
        self.add_a_tournament_frame = None
        self.match_frame = None

        self.rounds_list = []
        self.players_couple_list = []
        self.match_results_list = []

        self._current_tournament = 0
        self.tournament_name_var = StringVar()
        self.tournament_location_var = StringVar()
        self.tournament_date_var = StringVar()
        self.tournament_round_number_var = StringVar()
        self.tournament_time_control_var = StringVar()
        self.tournament_description_var = StringVar()

        self.round_number_var = StringVar()
        self.round_start_time_var = StringVar()
        self.round_end_time_var = StringVar()
        self.match_first_player_var = StringVar()
        self.match_second_player_var = StringVar()
        self.match_first_player_score_var = StringVar()
        self.match_second_player_score_var = StringVar()
        
    def activate_debug(self, is_debug):
        if is_debug == 'ON':
            dummy_tournaments_list = self.my_controller.get_dummy_tournaments_list()
            for dummy_tournament in dummy_tournaments_list:
                self.tree.insert('', END, values=dummy_tournament)
        else:
            self.load_tournaments_list_in_view()

    def item_selected(self, event, tree):
        logging.debug(f'ChessMainViews : tournaments nb item selected={len(self.tree.selection())}')
        if len(self.tree.selection()) == 0:
            pass
        elif len(self.tree.selection()) != 1:
            messagebox.showerror('Error', 'Select only one entry')
            return False
        else:
            selected_item = self.tree.selection()[0]
            item = self.tree.item(selected_item)
            tournament = item['values']
            self.my_controller.set_selected_tournament(tournament)
            # show a message
            # self.tournament_name_var.set(tournament[0])
            # self.tournament_location_var.set(tournament[1])
            # self.tournament_date_var.set(tournament[2])
            # self.tournament_round_number_var.set(tournament[3])
            # self.tournament_time_control_var.set(tournament[4])
            # self.tournament_description_var.set(tournament[5])
            return True

    def sort_tree_column(self, event):
        values = []
        heading = self.tree.identify("region", event.x, event.y)
        column = int(self.tree.identify_column(event.x)[1:])
        if heading == 'heading':
            for line in self.tree.get_children():
                values.append(self.tree.item(line)['values'])
            sorted_values = sorted(values, key=itemgetter(column - 1))
            self.tree.delete(*self.tree.get_children())
            for value in sorted_values:
                tournament = (value[0], value[1], value[2], value[3], value[4], value[5], value[6])
                self.tree.insert('', END, values=tournament)
        else:
            return None

    def clear_all_selection(self):
        for selection in self.tree.selection():
            self.tree.selection_remove(selection)

    def create_tree_widget(self, frame):
        style = ttk.Style()
        style.theme_use('clam')
        bg = style.lookup('TFrame', 'background')
        style.configure('Treeview.Heading', background=bg,  font=('calibre', 10, 'bold'))

        columns = ('name', 'location', 'date', 'round', 'time control', 'description')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree.bind('<Button>', lambda event: self.sort_tree_column(event))

        self.tournament_name_var = StringVar()
        self.tournament_location_var = StringVar()
        self.tournament_date_var = StringVar()
        self.tournament_round_number_var = StringVar()
        self.tournament_time_control_var = StringVar()
        self.tournament_description_var = StringVar()

        # define headings
        self.tree.heading('name', text='Name')
        self.tree.heading('location', text='Location')
        self.tree.heading('date', text='Date')
        self.tree.heading('round', text='Round')
        self.tree.heading('time control', text='Time Control')
        self.tree.heading('description', text='Description')

        self.tree.bind('<<TreeviewSelect>>', lambda event: self.item_selected(event, self.tree))
        self.tree.grid(row=0, column=0, sticky=NSEW)

        # add a scrollbar
        yscrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.grid(row=0, column=1, sticky='ns')

        xscrollbar = ttk.Scrollbar(frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=xscrollbar.set)
        xscrollbar.grid(row=1, column=0, sticky='ew')

        self.activate_debug(self.is_debug)

    def load_tournaments_list_in_view(self):
        logging.debug(f'ChessMainViews :  : load_tournaments_list_in_view')
        self.clear_tournaments_list()
        tournaments_list = self.my_controller.load_tournaments_list()
        logging.info(tournaments_list)
        for tournament in tournaments_list:
            self.tree.insert('', END, values=tournament)
        self.clear_all_selection()

    def show_tournaments_list_frame(self):
        self.tree_frame = LabelFrame(self.main_window, text='Tournaments list')
        self.tree_frame.pack()
        self.create_tree_widget(self.tree_frame)

    def show_match_frame(self):
        self.tree_frame = LabelFrame(self.main_window, text='Round')
        self.match_frame.pack()
        
    def add_players_list(self):
        tournament = self.my_controller.get_selected_tournament()
        if tournament is None:
            messagebox.showerror('Error', 'No tournament selected')
            return False

        retval = self.my_controller.assign_selected_players_to_selected_tournament()
        if retval:
            messagebox.showerror('Error', retval)
            return retval
        else:
            messagebox.showinfo('Info', 'Players have been added')
            return False

    def show_actions_frame(self):
        self.action_frame = LabelFrame(self.main_window, text='Actions')
        self.action_frame.pack()

        load_btn = Button(self.action_frame, text='Load', command=lambda: self.load_tournaments_list_in_view())
        load_btn.grid(row=0, column=0, padx=10, pady=10)
        save_btn = Button(self.action_frame, text='Report', command=lambda: self.generate_report())
        save_btn.grid(row=0, column=1, padx=10, pady=10)
        add_players_btn = Button(self.action_frame, text='Add Players', command=lambda: self.add_players_list())
        add_players_btn.grid(row=0, column=2, padx=10, pady=10)
        start_tournament_btn = Button(self.action_frame, text='Start', command=lambda: self.start_tournament())
        start_tournament_btn.grid(row=0, column=3, padx=10, pady=10)
        continue_tournament = Button(self.action_frame, text='Continue', command=lambda: self.continue_tournament())
        continue_tournament.grid(row=0, column=4, padx=10, pady=10)
        close_btn = Button(self.action_frame, text='Close', command=lambda: self.hide_all())
        close_btn.grid(row=0, column=5, padx=10, pady=10)

    def show_all(self):
        if self.is_already_created is False:
            self.show_tournaments_list_frame()
            self.show_actions_frame()
            self.show_round_match_frame()
            self.show_add_a_tournament_frame()
            self.is_already_created = True
        else:
            self.tree_frame.pack()
            self.action_frame.pack()
            self.match_frame.pack()
            self.add_a_tournament_frame.pack()
        self.set_visible()



    def hide_all(self):
        if self.is_already_created is True:
            self.tree_frame.pack_forget()
            self.action_frame.pack_forget()
            # self.change_a_player_rank_frame.pack_forget()
            self.match_frame.pack_forget()
            self.add_a_tournament_frame.pack_forget()
            self.set_not_visible()

    def clear_tournaments_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def clear_round_match_form(self):
        self.round_number_var.set('')
        self.round_start_time_var.set('')
        self.round_end_time_var.set('')
        self.match_first_player_var.set('')
        self.match_second_player_var.set('')
        self.match_first_player_score_var.set('')
        self.match_second_player_score_var.set('')

    def generate_report(self):
        filetypes = (('text files', '*.csv'), ('All files', '*.*'))
        try:
            file = filedialog.asksaveasfile(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
            file.write(f"'name','location','date','round','time control','description', 'tournament id'\n")
            for line in self.tree.get_children():
                values = self.tree.item(line)['values']
                file.write(f'{values[0]},{values[1]},{values[2]},{values[3]},{values[4]},{values[5]},{values[6]}\n')
            file.close()
        except Exception as error:
            print(f'Unexpected exception in generate_report(): {error}')

    def show_round_match_frame(self):
        self.match_frame = LabelFrame(self.main_window, text='Round/Match')
        self.match_frame.pack()
        string_var_list = [self.round_number_var,
                           self.round_start_time_var,
                           self.round_end_time_var,
                           self.match_first_player_var,
                           self.match_second_player_var,
                           self.match_first_player_score_var,
                           self.match_second_player_score_var]
        ChessTournamentsView.fill_a_match_form(self.match_frame, string_var_list)
        match_frame = Button(self.match_frame, text='Commit', command=self.commit_match)
        match_frame.grid(row=2, column=0)

    def start_tournament(self):
        tournament = self.my_controller.get_selected_tournament()
        if tournament is None:
            messagebox.showerror('Error', 'No tournament selected')
            return False

        self.rounds_list, self.players_couple_list, tournament = self.my_controller.get_rounds_players_couple_list()
        round_id = len(self.rounds_list) + 1

        if round_id > self.my_controller.get_max_rounds_number():
            messagebox.showinfo('Info', 'This tournament has been completed')
            return False
        # elif round_id == 1:
        #     messagebox.showerror('Error', 'This tournament has been started')
        #     return False
        elif len(self.players_couple_list) == 0:
            messagebox.showerror('Error', 'No players have been added')
            return False
        elif len(self.players_couple_list) != 0:
            start_time = self.my_controller.get_current_time()
            self.round_number_var.set(str(round_id))
            self.round_start_time_var.set(start_time)
            self.match_first_player_var.set(self.players_couple_list[0][0])
            self.match_second_player_var.set(self.players_couple_list[1][0])
            return True
        else:
            messagebox.showerror('Error', 'Deadly case')
            return False

    def set_tournament_completed(self):
        self.rounds_list = []
        self.players_couple_list = []
        self.match_results_list = []

    def continue_tournament(self):
        logging.debug(f'ChessMainViews : continue_tournament')
        tournament = self.my_controller.get_selected_tournament()
        if tournament is None:
            messagebox.showerror('Error', 'No tournament selected')
            return False

        self.rounds_list, self.players_couple_list, tournament = self.my_controller.get_rounds_players_couple_list(update_to_make=True)
        logging.info(f'ChessMainViews : self.rounds_list = {self.rounds_list}')
        logging.info(f'ChessMainViews : self.players_couple_list = {self.players_couple_list}')

        round_id = len(self.rounds_list) + 1
        logging.info(f'ChessMainViews : round_id = {round_id}')
        # if tournament is None:
        #     messagebox.showerror('Error', 'Focus lost on selected tournament\nPlease reselect')
        #     return False
        if round_id > self.my_controller.get_max_rounds_number():
            self.set_tournament_completed()
            self.my_controller.set_tournament_completed()
            self.clear_round_match_form()
            messagebox.showinfo('Info', 'This tournament has been completed')
            return False
        elif len(self.players_couple_list) == 0 and round_id == 1:
            messagebox.showerror('Error', 'Tournament has not been started')
            return False
        elif len(self.players_couple_list) != 0:
            logging.debug(f'ChessMainViews : continue_tournament - case len(self.players_couple_list) != 0:')
            self.round_number_var.set(str(round_id))
            start_time = self.my_controller.get_current_time()
            self.round_start_time_var.set(start_time)
            self.match_first_player_var.set(self.players_couple_list[0][0])
            self.match_second_player_var.set(self.players_couple_list[1][0])
            return True
        else:
            messagebox.showerror('Error', 'Deadly case')
            return False

    def commit_match(self):
        logging.debug(f'ChessMainViews : commit_match')
        round_number = self.round_number_var.get()
        round_start_time = self.round_start_time_var.get()
        round_end_time = self.round_end_time_var.get()
        if len(self.players_couple_list) != 0:
            match_first_player = self.match_first_player_var.get()
            match_second_player = self.match_second_player_var.get()
            match_first_player_score = self.match_first_player_score_var.get()
            match_second_player_score = self.match_second_player_score_var.get()
            if ChessUtils.check_int('Name', round_number) is False or \
                    ChessUtils.check_str('FirstPlayer', match_first_player) is False or \
                    ChessUtils.check_str('SecondPlayer', match_second_player) is False or \
                    ChessUtils.check_time('StartTime', round_start_time) is False or \
                    ChessUtils.check_enumerate('FirstPlayerScore',
                                               match_first_player_score, ['0', '0.5', '1']) is False or \
                    ChessUtils.check_enumerate('SecondPlayerScore',
                                               match_second_player_score, ['0', '0.5', '1']) is False or \
                    ChessUtils.check_score('PlayerScores', match_first_player_score, match_second_player_score) is False:
                return False

            match_first_player_id = self.players_couple_list[0][1]
            match_second_player_id = self.players_couple_list[1][1]
            a_match = [round_number,
                        round_start_time,
                        round_end_time,
                        [match_first_player, match_first_player_id, match_first_player_score],
                        [match_second_player, match_second_player_id, match_second_player_score]
                       ]

            self.match_results_list.append(a_match)

            logging.info(f'ChessMainViews : (1) couples_list={self.players_couple_list}')
            logging.info(f'ChessMainViews : (1) round={a_match}')
            logging.info(f'ChessMainViews : (1) len={len(self.match_results_list)} result={self.match_results_list}')

            del self.players_couple_list[0:2]

            self.match_first_player_score_var.set('')
            self.match_second_player_score_var.set('')

            if len(self.players_couple_list) != 0:
                self.match_first_player_var.set(self.players_couple_list[0][0])
                self.match_second_player_var.set(self.players_couple_list[1][0])
            else:
                self.round_end_time_var.set(self.my_controller.get_current_time())
                round_end_time = self.round_end_time_var.get()
                round_number, status = self.my_controller.update_a_match_results_list_round(round_number,
                                                                                    round_start_time,
                                                                                    round_end_time,
                                                                                    self.match_results_list)

                # self.match_results_list.append(a_match)

                logging.info(f'ChessMainViews : (2) couples_list={self.players_couple_list}')
                logging.info(f'ChessMainViews : (2) round={a_match}')
                logging.info(f'ChessMainViews : (2) len={len(self.match_results_list)} result={self.match_results_list}')

                messagebox.showinfo('Info', f'Round {round_number} result has been inserted in DB')
                self.match_results_list = []
                self.continue_tournament()
        else:
            messagebox.showerror('Info', f'ChessMainViews : commit_match (1) - Deadly case')
            # self.round_end_time_var.set(self.my_controller.get_current_time())
            # round_end_time = self.round_end_time_var.get()
            # round_number, status = self.my_controller.update_a_match_results_list_round(round_number,
            #                                                                     round_start_time,
            #                                                                     round_end_time,
            #                                                                     self.match_results_list)
            # messagebox.showinfo('Info', f'Round {round_number} result has been inserted in DB')
            # self.continue_tournament()

    @staticmethod
    def fill_a_match_form(frame, string_var_list):
        round_label = Label(frame, text='Round', font=('calibre', 10, 'bold'))
        round_entry = Entry(frame, textvariable=string_var_list[0], font=('calibre', 10, 'normal'), state=DISABLED)

        start_time_label = Label(frame, text='StartTime', font=('calibre', 10, 'bold'))
        start_time_entry = Entry(frame, textvariable=string_var_list[1], font=('calibre', 10, 'normal'), state=DISABLED)

        end_time_label = Label(frame, text='EndTime', font=('calibre', 10, 'bold'))
        end_time_entry = Entry(frame, textvariable=string_var_list[2], font=('calibre', 10, 'normal'), state=DISABLED)

        first_player_label = Label(frame, text='FirstPlayer', font=('calibre', 10, 'bold'))
        first_player_entry = Entry(frame, textvariable=string_var_list[3], state=DISABLED)

        second_player_label = Label(frame, text='SecondPlayer', font=('calibre', 10, 'bold'))
        second_player_entry = Entry(frame, textvariable=string_var_list[4], state=DISABLED)

        first_player_score_label = Label(frame, text='FirstPlayerScore', font=('calibre', 10, 'bold'))
        first_player_score_entry = Spinbox(frame, textvariable=string_var_list[5],
                                           values=('', '0', '0.5', '1'), font=('calibre', 10, 'normal'))

        second_player_score_label = Label(frame, text='SecondPlayerScore', font=('calibre', 10, 'bold'))
        second_player_score_entry = Spinbox(frame, textvariable=string_var_list[6],
                                          values=('', '0', '0.5', '1'), font=('calibre', 10, 'normal'))

        round_label.grid(row=0, column=0)
        start_time_label.grid(row=0, column=1)
        end_time_label.grid(row=0, column=2)
        first_player_label.grid(row=0, column=3)
        second_player_label.grid(row=0, column=4)
        first_player_score_label.grid(row=0, column=5)
        second_player_score_label.grid(row=0, column=6)

        round_entry.grid(row=1, column=0)
        start_time_entry.grid(row=1, column=1)
        end_time_entry.grid(row=1, column=2)
        first_player_entry.grid(row=1, column=3)
        second_player_entry.grid(row=1, column=4)
        first_player_score_entry.grid(row=1, column=5)
        second_player_score_entry.grid(row=1, column=6)
        
    def show_add_a_tournament_frame(self):
        self.add_a_tournament_frame = LabelFrame(self.main_window, text='Add a tournament')
        self.add_a_tournament_frame.pack()
        string_var_list = [self.tournament_name_var,
                           self.tournament_location_var,
                           self.tournament_date_var,
                           self.tournament_round_number_var,
                           self.tournament_time_control_var,
                           self.tournament_description_var]

        ChessTournamentsView.fill_a_tournament_form(self.add_a_tournament_frame, string_var_list)
        add_tournament_button = Button(self.add_a_tournament_frame, text='Add', command=self.add_a_tournament)
        add_tournament_button.grid(row=2, column=0)

    @staticmethod
    def fill_a_tournament_form(frame, string_var_list, widget_state=NORMAL):
        name_label = Label(frame, text='Name', font=('calibre', 10, 'bold'))
        name_entry = Entry(frame, textvariable=string_var_list[0], font=('calibre', 10, 'normal'), state=widget_state)

        location_label = Label(frame, text='location', font=('calibre', 10, 'bold'))
        location_entry = Entry(frame, textvariable=string_var_list[1], font=('calibre', 10, 'normal'), state=widget_state)

        date_label = Label(frame, text='Date', font=('calibre', 10, 'bold'))
        date_entry = DateEntry(frame, textvariable=string_var_list[2], date_pattern='dd/mm/yyyy', state=widget_state)
        date_entry.delete(0, END)

        round_label = Label(frame, text='Round', font=('calibre', 10, 'bold'))
        round_entry = Entry(frame, textvariable=string_var_list[3], state=widget_state)

        time_control_label = Label(frame, text='Time Control', font=('calibre', 10, 'bold'))
        time_control_entry = Spinbox(frame, values=('', 'Blitz', 'Bullet', 'Fast'), textvariable=string_var_list[4], state=widget_state)

        description_label = Label(frame, text='Description', font=('calibre', 10, 'bold'))
        description_entry = Entry(frame, textvariable=string_var_list[5], font=('calibre', 10, 'normal'))

        name_label.grid(row=0, column=0)
        location_label.grid(row=0, column=1)
        date_label.grid(row=0, column=2)
        round_label.grid(row=0, column=3)
        time_control_label.grid(row=0, column=4)
        description_label.grid(row=0, column=5)

        name_entry.grid(row=1, column=0)
        location_entry.grid(row=1, column=1)
        date_entry.grid(row=1, column=2)
        round_entry.grid(row=1, column=3)
        time_control_entry.grid(row=1, column=4)
        description_entry.grid(row=1, column=5)

    def add_a_tournament(self):
        tournament_name = self.tournament_name_var.get()
        tournament_location = self.tournament_location_var.get()
        tournament_date = self.tournament_date_var.get()
        tournament_round_number = self.tournament_round_number_var.get()
        tournament_time_control = self.tournament_time_control_var.get()
        tournament_description = self.tournament_description_var.get()
        if ChessUtils.check_str('Name', tournament_name) is False or \
                ChessUtils.check_str('Location', tournament_location) is False or \
                ChessUtils.check_date('Date', tournament_date) is False or \
                ChessUtils.check_int('Round', tournament_round_number) is False or \
                ChessUtils.check_enumerate('time_control',
                                           tournament_time_control, ['Blitz', 'Bullet', 'Fast']) is False or \
                ChessUtils.check_str('Description', tournament_description) is False:
            return False

        tournament = (tournament_name, tournament_location, tournament_date, tournament_round_number, tournament_time_control,
                      tournament_description, self.my_controller.get_tournament_id())
        logging.debug(f'ChessMainViews : add a tournament {tournament}')
        self.my_controller.save_a_tournament(tournament)

        self.tree.insert('', END, values=tournament)
        self.tournament_name_var.set("")
        self.tournament_location_var.set("")
        self.tournament_date_var.set("")
        self.tournament_round_number_var.set("")
        self.tournament_time_control_var.set("")
        self.tournament_description_var.set("")
        return True



"""
    ChessPlayersView
"""
class ChessPlayersView(ChessBasicView):
    def __init__(self, controller):
        super().__init__(controller)
        self.my_controller = controller
        # self.is_built = False
        # self.is_debug = None

        # declaring string variable
        self.last_name_var = StringVar()
        self.first_name_var = StringVar()
        self.birthdate_var = StringVar()
        self.gender_var = StringVar()
        self.rank_var = StringVar()

        self.last_name_var2 = StringVar()
        self.first_name_var2 = StringVar()
        self.birthdate_var2 = StringVar()
        self.gender_var2 = StringVar()
        self.rank_var2 = StringVar()

        self.action_frame = None
        self.add_a_player_frame = None
        self.change_a_player_rank_frame = None

    def item_selected(self, event, tree):
        logging.debug(f'ChessMainViews : player nb item selected={len(self.tree.selection())}')
        nb_selected = len(self.tree.selection())
        selected_players_list = []
        if nb_selected == 1:
            selected_item = self.tree.selection()[0]
            item = self.tree.item(selected_item)
            player = item['values']
            # show a message
            self.last_name_var2.set(player[0])
            self.first_name_var2.set(player[1])
            self.birthdate_var2.set(player[2])
            self.gender_var2.set(player[3])
            self.rank_var2.set(player[4])
            return True
        elif nb_selected % 2:
            messagebox.showerror('Error', 'select an even number of entries')
            return False
        else:
            self.last_name_var2.set("")
            self.first_name_var2.set("")
            self.birthdate_var2.set("")
            self.gender_var2.set("")
            self.rank_var2.set("")
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                player = item['values']
                selected_players_list.append(player)
            self.my_controller.set_selected_players_list(selected_players_list)

            return True

    def clear_players_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_players_list_in_view(self):
        logging.debug(f'ChessMainViews :  : load_players_list_in_view')
        self.clear_players_list()
        players_list = self.my_controller.load_players_list()
        logging.info(players_list)
        for player in players_list:
            self.tree.insert('', END, values=player)
        self.my_controller.set_player_id(len(players_list))

    def modify_a_player_rank(self):
        logging.debug(f'ChessMainViews :  : modify_a_player_rank')
        selected = self.tree.focus()
        if ChessUtils.check_int('Rank', self.rank_var2.get()) is False:
            return False
        values = self.tree.item(selected, 'values')
        player = (values[0], values[1], values[2], values[3], self.rank_var2.get(), values[5])
        logging.info(f'ChessMainViews : {player}')
        self.my_controller.update_a_player_rank(player, self.rank_var2.get())
        self.tree.item(selected, text='', values=player)
        self.last_name_var2.set("")
        self.first_name_var2.set("")
        self.birthdate_var2.set("")
        self.gender_var2.set("")
        self.rank_var2.set("")
        return True

    def add_a_player(self):
        last_name = self.last_name_var.get()
        first_name = self.first_name_var.get()
        birthdate = self.birthdate_var.get()
        gender = self.gender_var.get()
        rank = self.rank_var.get()
        if ChessUtils.check_str('Last Name', last_name) is False or \
            ChessUtils.check_str('First Name', first_name) is False or \
            ChessUtils.check_date('Birthdate', birthdate) is False or \
            ChessUtils.check_enumerate('Gender', gender, ['Male', 'Female']) is False or \
            ChessUtils.check_int('Rank', rank) is False:
            return False

        player = (last_name, first_name, birthdate, gender, rank, self.my_controller.get_player_id())
        logging.debug(f'ChessMainViews : add a player {player}')
        self.my_controller.save_a_player(player)

        self.tree.insert('', END, values=player)
        self.last_name_var.set("")
        self.first_name_var.set("")
        self.birthdate_var.set("")
        self.gender_var.set("")
        self.rank_var.set("")
        return True

    def sort_tree_column(self, event):
        values = []
        heading = self.tree.identify("region", event.x, event.y)
        column = int(self.tree.identify_column(event.x)[1:])
        if heading == 'heading':
            for line in self.tree.get_children():
                values.append(self.tree.item(line)['values'])
            sorted_values = sorted(values, key=itemgetter(column - 1))
            self.tree.delete(*self.tree.get_children())
            for value in sorted_values:
                player = (value[0], value[1], value[2], value[3], value[4], value[5])
                self.tree.insert('', END, values=player)
        else:
            return None

    def generate_report(self):
        filetypes = (('text files', '*.csv'), ('All files', '*.*'))
        try:
            file = filedialog.asksaveasfile(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
            file.write(f"'last name','first name','birthdate','gender','rank','player id'\n")
            for line in self.tree.get_children():
                values = self.tree.item(line)['values']
                file.write(f'{values[0]},{values[1]},{values[2]},{values[3]},{values[4]},{values[5]}\n')
            file.close()
        except Exception as error:
            print(f'Unexpected exception in generate_report(): {error}')

    def activate_debug(self, is_debug):
        if is_debug == 'ON':
            dummy_players_list = self.my_controller.get_dummy_players_list()
            for dummy_player in dummy_players_list:
                self.tree.insert('', END, values=dummy_player)
        else:
            self.load_players_list_in_view()

    def create_tree_widget(self, frame):
        style = ttk.Style()
        style.theme_use('clam')
        bg = style.lookup('TFrame', 'background')
        style.configure('Treeview.Heading', background=bg,  font=('calibre', 10, 'bold'))

        columns = ('last name', 'first name', 'birthdate', 'gender', 'rank')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree.bind('<Button>', lambda event: self.sort_tree_column(event))

        # define headings
        self.tree.heading('last name', text='Last Name')
        self.tree.heading('first name', text='First Name')
        self.tree.heading('birthdate', text='Birthdate')
        self.tree.heading('gender', text='Gender')
        self.tree.heading('rank', text='Rank')

        self.tree.bind('<<TreeviewSelect>>', lambda event: self.item_selected(event, self.tree))
        self.tree.grid(row=0, column=0, sticky=NSEW)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.activate_debug(self.is_debug)

    def show_players_list_frame(self):
        self.tree_frame = LabelFrame(self.main_window, text='Players list')
        self.tree_frame.pack()
        self.create_tree_widget(self.tree_frame)

    def show_actions_frame(self):
        self.action_frame = LabelFrame(self.main_window, text='Actions')
        self.action_frame.pack()

        load_btn = Button(self.action_frame, text='Load', command=lambda: self.load_players_list_in_view())
        load_btn.grid(row=0, column=0, padx=10, pady=10)
        save_btn = Button(self.action_frame, text='Report', command=lambda: self.generate_report())
        save_btn.grid(row=0, column=1, padx=10, pady=10)
        close_btn = Button(self.action_frame, text='Close', command=lambda: self.hide_all())
        close_btn.grid(row=0, column=2, padx=10, pady=10)

    @staticmethod
    def fill_a_player_form(frame, string_var_list, widget_state=NORMAL):
        last_name_label = Label(frame, text='Last Name', font=('calibre', 10, 'bold'))
        last_name_entry = Entry(frame, textvariable=string_var_list[0], font=('calibre', 10, 'normal'), state=widget_state)

        first_name_label = Label(frame, text='First Name', font=('calibre', 10, 'bold'))
        first_name_entry = Entry(frame, textvariable=string_var_list[1], font=('calibre', 10, 'normal'), state=widget_state)

        birthdate_label = Label(frame, text='Birthdate', font=('calibre', 10, 'bold'))
        if widget_state == 'normal':
            birthdate_entry = DateEntry(frame, textvariable=string_var_list[2], date_pattern='dd/mm/yyyy', state=widget_state)
            birthdate_entry.delete(0, END)

            gender_label = Label(frame, text='Gender', font=('calibre', 10, 'bold'))
            gender_entry = Spinbox(frame, values=('', 'Male', 'Female'), textvariable=string_var_list[3], state=widget_state)
        else:
            birthdate_entry = Entry(frame, textvariable=string_var_list[2], font=('calibre', 10, 'normal'), state=widget_state)
            birthdate_entry.delete(0, END)

            gender_label = Label(frame, text='Gender', font=('calibre', 10, 'bold'))
            gender_entry = Entry(frame, textvariable=string_var_list[3], font=('calibre', 10, 'normal'), state=widget_state)

        rank_label = Label(frame, text='Rank', font=('calibre', 10, 'bold'))
        rank_entry = Entry(frame, textvariable=string_var_list[4], font=('calibre', 10, 'normal'))

        last_name_label.grid(row=0, column=0)
        first_name_label.grid(row=0, column=1)
        birthdate_label.grid(row=0, column=2)
        gender_label.grid(row=0, column=3)
        rank_label.grid(row=0, column=4)

        last_name_entry.grid(row=1, column=0)
        first_name_entry.grid(row=1, column=1)
        birthdate_entry.grid(row=1, column=2)
        gender_entry.grid(row=1, column=3)
        rank_entry.grid(row=1, column=4)

    def show_add_a_player_frame(self):
        self.add_a_player_frame = LabelFrame(self.main_window, text='Add a player')
        self.add_a_player_frame.pack()
        string_var_list = [self.last_name_var, self.first_name_var, self.birthdate_var, self.gender_var, self.rank_var]

        ChessPlayersView.fill_a_player_form(self.add_a_player_frame, string_var_list)
        add_player_button = Button(self.add_a_player_frame, text='Add', command=self.add_a_player)
        add_player_button.grid(row=2, column=0)

    def show_change_a_player_rank_frame(self):
        self.change_a_player_rank_frame = LabelFrame(self.main_window, text='Modify Rank')
        self.change_a_player_rank_frame.pack()

        string_var_list = [self.last_name_var2, self.first_name_var2, self.birthdate_var2, self.gender_var2, self.rank_var2]
        ChessPlayersView.fill_a_player_form(self.change_a_player_rank_frame, string_var_list, widget_state=DISABLED)
        change_a_player_rank_button = Button(self.change_a_player_rank_frame, text='Modify', command=self.modify_a_player_rank)
        change_a_player_rank_button.grid(row=2, column=0)

    def show_all(self):
        if self.is_already_created is False:
            self.show_players_list_frame()
            self.show_actions_frame()
            self.show_change_a_player_rank_frame()
            self.show_add_a_player_frame()
            self.is_already_created = True
        else:
            self.tree_frame.pack()
            self.action_frame.pack()
            self.change_a_player_rank_frame.pack()
            self.add_a_player_frame.pack()
        self.set_visible()

    def hide_all(self):
        if self.is_already_created is True:
            self.tree_frame.pack_forget()
            self.action_frame.pack_forget()
            self.change_a_player_rank_frame.pack_forget()
            self.add_a_player_frame.pack_forget()
            self.set_not_visible()

class VirtualView:
    def __init__(self):
        pass

    def display_interface(self):
        pass


class ChessMainView(VirtualView):
    def __init__(self):
        super().__init__()

        self.my_controller = None
        self.player_view = None
        self.tournament_view = None

        self.main_window = Tk()

        self.main_window.title("Chess Tournaments")
        self.main_window.geometry("1100x520")
        self.main_window.minsize(1100, 520)

        menu_bar = Menu(self.main_window)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 File", menu=file_menu)

        player_menu = Menu(menu_bar, tearoff=0)
        # player_menu.add_command(label="🔎 Display", command=lambda: self.player_view.show_all())
        player_menu.add_command(label="🔎 Display", command=lambda: ChessMainView.toggle_view(self.player_view, self.tournament_view))
        player_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 Players", menu=player_menu)

        tournament_list_menu = Menu(menu_bar, tearoff=0)
        # tournament_list_menu.add_command(label="🔎 Display", command=lambda: self.tournament_view.show_all())
        tournament_list_menu.add_command(label="🔎 Display", command=lambda: ChessMainView.toggle_view(self.tournament_view, self.player_view))
        tournament_list_menu.add_command(label="🗙 Exit", command=self.main_window.quit)

        # tournament_menu.add_command(label="🔎 Create", command=lambda: print('Not implemented'))
        # tournament_menu.add_command(label="🔎 Start", command=lambda: print('Not implemented'))
        # tournament_menu.add_command(label="🔎 Suspend", command=lambda: print('Not implemented'))
        # tournament_menu.add_command(label="🔎 Resume", command=lambda: print('Not implemented'))
        # tournament_menu.add_command(label="🔎 Cancel", command=lambda: print('Not implemented'))
        # tournament_menu.add_command(label="🗙 Exit", command=lambda: print('Not implemented'))
        menu_bar.add_cascade(label="📁 Tournaments", menu=tournament_list_menu)

        self.main_window.config(menu=menu_bar)

    def set_my_controller(self, controller):
        self.my_controller = controller
        self.player_view = ChessPlayersView(controller)
        self.tournament_view = ChessTournamentsView(controller)

    @staticmethod
    def toggle_view(first_view, second_view):
        if second_view.is_visible():
            second_view.hide_all()
        first_view.show_all()

    def display_interface(self):
        self.main_window.mainloop()

