import configparser
import logging
from operator import itemgetter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkcalendar import DateEntry
from ChessUtils import ChessUtils
from ChessControllers.ChessMainControllers import ChessMainController


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

    def generic_display_report(self, a_title):
        new_window = Tk()
        new_window.title(a_title)
        new_window.geometry("1100x520")
        new_window.minsize(1100, 520)
        new_frame = Frame(new_window)
        new_frame.pack(fill='both')
        read_only_text = Text(new_frame)
        new_frame.pack(expand=True, fill='both')
        read_only_text.pack(expand=True, fill='both')
        return read_only_text

    def generate_report(self):
        pass

    def display_report(self):
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

        self.tournament_report_btn = None
        self.tournament_name_dict = None

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
            return True

    def clear_tree_selection(self):
        for i in self.tree.selection():
            self.tree.selection_remove(i)

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
        style.configure('Treeview.Heading', background=bg, font=('calibre', 10, 'bold'))

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

        self.activate_debug(self.is_debug)

    def load_tournaments_list_in_view(self):
        logging.debug(f'ChessMainViews : load_tournaments_list_in_view')
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

    def display_report_players_ordered_by_name(self):
        if self.my_controller.get_selected_tournament() is not None:
            result_list = self.my_controller.get_tournament_players_ordered_by_name()
            read_only_text = self.generic_display_report('Tournament players ordered by name')
            read_only_text.insert(INSERT,
                                  '{:25s} {:25s} {:25s} {:10s} {:10s}\n'.format("last Name", "First Nme", "Birthdate",
                                                                                "Gender", "Rank"))
            for values in result_list:
                read_only_text.insert(INSERT,
                                      '{:25s} {:25s} {:25s} {:10s} {:10s}\n'.format(values[0], values[1], values[2],
                                                                                    values[3], str(values[4])))
        else:
            messagebox.showwarning("Warning", 'Did you select a tournament?\nOr try to reselect again\n')

    def display_report_a_tournament_players_ordered_by_rank(self):
        if self.my_controller.get_selected_tournament() is not None:
            result_list = self.my_controller.get_tournament_players_ordered_by_rank('Players ordered by rank')
            read_only_text = self.generic_display_report('Tournament players ordered by rank')
            read_only_text.insert(INSERT,
                                  '{:25s} {:25s} {:25s} {:25s} {:25s}\n'.format("last Name", "First Nme", "Birthdate",
                                                                                "Gender", "Rank"))
            for values in result_list:
                read_only_text.insert(INSERT,
                                      '{:25s} {:25s} {:25s} {:25s} {:25s}\n'.format(values[0], values[1], values[2],
                                                                                    values[3], str(values[4])))
        else:
            messagebox.showwarning("Warning", 'Did you select a tournament?\nOr try to reselect again\n')

    def display_report_all_tournaments(self):
        result_list = self.my_controller.get_all_tournaments()
        logging.info(f'ChessMainViews : display_report_all_tournaments : result_list')
        read_only_text = self.generic_display_report('All tournaments')
        read_only_text.insert(INSERT,
                              '{:25s} {:25s} {:10s} {:6s} {:12s} {:25s}\n'.format("Name", "Location", "Date", 'Rounds',
                                                                                  "Time Control", "Description"))

        for values in result_list:
            read_only_text.insert(INSERT, '{:25s} {:25s} {:10s} {:6s} {:12s} {:25s}\n'.format(values[0], values[1],
                                                                                              values[2],
                                                                                              str(values[3]),
                                                                                              str(values[4]),
                                                                                              values[5]))

    def display_report_a_tournament_rounds(self):
        logging.debug(f'ChessMainViews : display_report_a_tournament_rounds')
        if self.my_controller.get_selected_tournament() is not None:
            result_list = self.my_controller.get_a_tournament_rounds()
            logging.info(f'ChessMainViews : display_report_a_tournament_rounds : result_list = {result_list}')
            read_only_text = self.generic_display_report('Tournament rounds')
            read_only_text.insert(INSERT,
                                  '{:10s} {:10} {:10s}\n'.format("Name", "Start Date", 'End Date'))
            for values in result_list:
                read_only_text.insert(INSERT,
                                      '{:10s} {:10} {:10s}\n'.format('Round ' + values[0], values[1], values[2]))
        else:
            messagebox.showwarning("Warning", 'Did you select a tournament?\nOr try to reselect again\n')

    def display_report_a_tournament_matches(self):
        if self.my_controller.get_selected_tournament() is not None:
            logging.debug(f'ChessMainViews : display_report_a_tournament_matches')
            players_list, result_list = self.my_controller.get_a_tournament_matches()
            logging.info(f'ChessMainViews : display_report_a_tournament_matches : matches = {result_list}')
            read_only_text = self.generic_display_report('Tournament matches')
            read_only_text.insert(INSERT,
                                  '{:25s} {:10s}\n'.format("Name", "Rank"))
            for values in players_list:
                read_only_text.insert(INSERT,
                                      '{:25s} {:10s}\n'.format(values[0], str(values[4])))

            read_only_text.insert(INSERT, '\n\n')

            read_only_text.insert(INSERT,
                                  '{:10s} {:25s} {:5s} {:25s} {:5s}\n'.format('Round', "Name", "Score", 'Name',
                                                                              'Score'))

            for values in result_list:
                read_only_text.insert(INSERT, '{:10s} {:25s} {:5s} {:25s} {:5s}\n'.format(values[0],
                                                                                          values[1],
                                                                                          values[2],
                                                                                          values[3],
                                                                                          values[4]))

            read_only_text.insert(INSERT,
                                  '\n\n{:25s} {:6s}\n'.format("Name", "Score"))
            result_list = self.my_controller.get_participants_score()
            for values in result_list:
                read_only_text.insert(INSERT,
                                      '{:25s} {:6s}\n'.format(values[0], str(values[1])))
        else:
            messagebox.showwarning("Warning", 'Did you select a tournament?\nOr try to reselect again\n')

    def display_a_tournament_report(self, name):
        logging.debug(f'ChessMainViews : display_a_report')

        if name == 'Players alphabetic order':
            self.display_report_players_ordered_by_name()
        elif name == 'Players rank order':
            self.display_report_a_tournament_players_ordered_by_rank()
        elif name == 'All tournaments':
            self.display_report_all_tournaments()
        elif name == 'All rounds':
            self.display_report_a_tournament_rounds()
        elif name == 'All matches':
            self.display_report_a_tournament_matches()
        else:
            messagebox.showerror('Error', 'Unknown selection')
        self.tournament_report_btn.selection_clear()
        self.tournament_name_dict[name].set('')

    def add_sub_menus_for_tournament_report(self):
        self.tournament_report_btn.menu = Menu(self.tournament_report_btn, tearoff=0)
        self.tournament_report_btn["menu"] = self.tournament_report_btn.menu

        self.tournament_name_dict = {'Players alphabetic order': IntVar(), 'Players rank order': IntVar(),
                                     'All tournaments': IntVar(), 'All rounds': IntVar(), 'All matches': IntVar()}
        for name, var in self.tournament_name_dict.items():
            self.tournament_report_btn.menu.add_checkbutton(label=name, variable=self.tournament_name_dict[name],
                                                            command=lambda n=name: self.display_a_tournament_report(n))

    def show_actions_frame(self):
        self.action_frame = LabelFrame(self.main_window, text='Actions')
        self.action_frame.pack()

        load_btn = Button(self.action_frame, text='Load', command=lambda: self.load_tournaments_list_in_view())
        load_btn.grid(row=0, column=0, padx=10, pady=10)

        self.tournament_report_btn = Menubutton(self.action_frame, text='Report', relief=RAISED, borderwidth=2)
        self.tournament_report_btn.grid(row=0, column=1, padx=10, pady=10)
        self.add_sub_menus_for_tournament_report()

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
            logging.error(f'Unexpected exception in generate_report(): {error}')

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
        next_match_frame = Button(self.match_frame, text='Next', command=self.next_match)
        next_match_frame.grid(row=2, column=0)
        # save_current_state_frame = Button(self.match_frame, text='Save', command=self.save_current_state)
        # save_current_state_frame.grid(row=2, column=0)

    def save_current_state(self):
        pass

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
            start_time = ChessMainController.get_current_time()
            self.round_number_var.set('Round ' + str(round_id))
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

        self.rounds_list, self.players_couple_list, tournament = self.my_controller.get_rounds_players_couple_list(
            update_to_make=True)
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
            self.round_number_var.set('Round ' + str(round_id))
            start_time = ChessMainController.get_current_time()
            self.round_start_time_var.set(start_time)
            self.match_first_player_var.set(self.players_couple_list[0][0])
            self.match_second_player_var.set(self.players_couple_list[1][0])
            return True
        else:
            messagebox.showerror('Error', 'Deadly case')
            return False

    def next_match(self):
        logging.debug(f'ChessMainViews : next_match')
        round_number = self.round_number_var.get()
        round_start_time = self.round_start_time_var.get()
        round_end_time = self.round_end_time_var.get()
        if len(self.players_couple_list) != 0:
            match_first_player = self.match_first_player_var.get()
            match_second_player = self.match_second_player_var.get()
            match_first_player_score = self.match_first_player_score_var.get()
            match_second_player_score = self.match_second_player_score_var.get()
            if ChessUtils.check_str('Round', round_number) is False or \
                    ChessUtils.check_str('FirstPlayer', match_first_player) is False or \
                    ChessUtils.check_str('SecondPlayer', match_second_player) is False or \
                    ChessUtils.check_time('StartTime', round_start_time) is False or \
                    ChessUtils.check_enumerate('FirstPlayerScore',
                                               match_first_player_score, ['0', '0.5', '1']) is False or \
                    ChessUtils.check_enumerate('SecondPlayerScore',
                                               match_second_player_score, ['0', '0.5', '1']) is False or \
                    ChessUtils.check_score('PlayerScores', match_first_player_score,
                                           match_second_player_score) is False:
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
                self.round_end_time_var.set(ChessMainController.get_current_time())
                round_end_time = self.round_end_time_var.get()
                round_number, status = self.my_controller.update_a_match_results_list_round(round_number,
                                                                                            round_start_time,
                                                                                            round_end_time,
                                                                                            self.match_results_list)

                # self.match_results_list.append(a_match)

                logging.info(f'ChessMainViews : (2) couples_list={self.players_couple_list}')
                logging.info(f'ChessMainViews : (2) round={a_match}')
                logging.info(
                    f'ChessMainViews : (2) len={len(self.match_results_list)} result={self.match_results_list}')

                messagebox.showinfo('Info', f'Round {round_number} result has been inserted in DB')
                self.match_results_list = []
                self.continue_tournament()
        else:
            messagebox.showerror('Info', f'ChessMainViews : commit_match (1) - Deadly case')

    @staticmethod
    def fill_a_match_form(frame, string_var_list):
        round_label = Label(frame, text='Round', font=('calibre', 10, 'bold'))
        round_entry = Entry(frame, textvariable=string_var_list[0], font=('calibre', 10, 'normal'), state=DISABLED)

        start_time_label = Label(frame, text='StartTime', font=('calibre', 10, 'bold'))
        start_time_entry = Entry(frame, textvariable=string_var_list[1], font=('calibre', 10, 'normal'),
                                 state=DISABLED)

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
        location_entry = Entry(frame, textvariable=string_var_list[1], font=('calibre', 10, 'normal'),
                               state=widget_state)

        date_label = Label(frame, text='Date', font=('calibre', 10, 'bold'))
        date_entry = DateEntry(frame, textvariable=string_var_list[2], date_pattern='dd/mm/yyyy', state=widget_state)
        date_entry.delete(0, END)

        round_label = Label(frame, text='Round', font=('calibre', 10, 'bold'))
        round_entry = Entry(frame, textvariable=string_var_list[3], state=widget_state)

        time_control_label = Label(frame, text='Time Control', font=('calibre', 10, 'bold'))
        time_control_entry = Spinbox(frame, values=('', 'Blitz', 'Bullet', 'Fast'), textvariable=string_var_list[4],
                                     state=widget_state)

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

        tournament = (tournament_name, tournament_location, tournament_date, tournament_round_number,
                      tournament_time_control, tournament_description, self.my_controller.get_tournament_id())
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

        self.players_report_btn = None
        self.players_name_dict = None

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

    def clear_players_list_selection(self):
        for item in self.tree.get_children():
            self.tree.remove(item)

    def load_players_list_in_view(self):
        logging.debug(f'ChessMainViews :  : load_players_list_in_view')
        self.clear_players_list_selection()
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
            logging.error(f'Unexpected exception in generate_report(): {error}')

    def display_report_players_ordered_by_name(self):
        result_list = self.my_controller.get_players_ordered_by_name()
        read_only_text = self.generic_display_report('Players ordered by name')
        read_only_text.insert(INSERT,
                              '{:25s} {:25s} {:25s} {:25s} {:25s}\n'.format("last Name", "First Nme", "Birthdate",
                                                                            "Gender", "Rank"))
        for values in result_list:
            read_only_text.insert(INSERT,
                                  '{:25s} {:25s} {:25s} {:25s} {:25s}\n'.format(values[0], values[1], values[2],
                                                                                values[3], str(values[4])))

    def display_report_a_tournament_players_ordered_by_rank(self):
        result_list = self.my_controller.get_players_ordered_by_rank()
        read_only_text = self.generic_display_report('Players ordered by rank')
        read_only_text.insert(INSERT,
                              '{:25s} {:25s} {:25s} {:25s} {:25s}\n'.format("last Name", "First Nme", "Birthdate",
                                                                            "Gender", "Rank"))
        for values in result_list:
            read_only_text.insert(INSERT,
                                  '{:25s} {:25s} {:25s} {:25s} {:25s}\n'.format(values[0], values[1], values[2],
                                                                                values[3], str(values[4])))

    def add_sub_menus_for_players_report(self):
        self.players_report_btn.menu = Menu(self.players_report_btn, tearoff=0)
        self.players_report_btn["menu"] = self.players_report_btn.menu

        self.players_name_dict = {'Players alphabetic order': IntVar(), 'Players rank order': IntVar()}
        for name, var in self.players_name_dict.items():
            self.players_report_btn.menu.add_checkbutton(label=name, variable=self.players_name_dict[name],
                                                         command=lambda n=name: self.display_a_players_report(n))

    def display_a_players_report(self, name):
        logging.debug(f'ChessMainViews : display_a_report')

        if name == 'Players alphabetic order':
            self.display_report_players_ordered_by_name()
        elif name == 'Players rank order':
            self.display_report_a_tournament_players_ordered_by_rank()
        else:
            messagebox.showerror('Error', 'Unknown selection')
        self.players_report_btn.selection_clear()
        self.players_name_dict[name].set('')

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
        style.configure('Treeview.Heading', background=bg, font=('calibre', 10, 'bold'))

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

        self.players_report_btn = Menubutton(self.action_frame, text='Report', relief=RAISED, borderwidth=2)
        self.players_report_btn.grid(row=0, column=1, padx=10, pady=10)
        self.add_sub_menus_for_players_report()

        close_btn = Button(self.action_frame, text='Close', command=lambda: self.hide_all())
        close_btn.grid(row=0, column=2, padx=10, pady=10)

    @staticmethod
    def fill_a_player_form(frame, string_var_list, widget_state=NORMAL):
        last_name_label = Label(frame, text='Last Name', font=('calibre', 10, 'bold'))
        last_name_entry = Entry(frame, textvariable=string_var_list[0], font=('calibre', 10, 'normal'),
                                state=widget_state)

        first_name_label = Label(frame, text='First Name', font=('calibre', 10, 'bold'))
        first_name_entry = Entry(frame, textvariable=string_var_list[1], font=('calibre', 10, 'normal'),
                                 state=widget_state)

        birthdate_label = Label(frame, text='Birthdate', font=('calibre', 10, 'bold'))
        if widget_state == 'normal':
            birthdate_entry = DateEntry(frame, textvariable=string_var_list[2], date_pattern='dd/mm/yyyy',
                                        state=widget_state)
            birthdate_entry.delete(0, END)

            gender_label = Label(frame, text='Gender', font=('calibre', 10, 'bold'))
            gender_entry = Spinbox(frame, values=('', 'Male', 'Female'), textvariable=string_var_list[3],
                                   state=widget_state)
        else:
            birthdate_entry = Entry(frame, textvariable=string_var_list[2], font=('calibre', 10, 'normal'),
                                    state=widget_state)
            birthdate_entry.delete(0, END)

            gender_label = Label(frame, text='Gender', font=('calibre', 10, 'bold'))
            gender_entry = Entry(frame, textvariable=string_var_list[3], font=('calibre', 10, 'normal'),
                                 state=widget_state)

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

        string_var_list = [self.last_name_var2, self.first_name_var2, self.birthdate_var2, self.gender_var2,
                           self.rank_var2]
        ChessPlayersView.fill_a_player_form(self.change_a_player_rank_frame, string_var_list, widget_state=DISABLED)
        change_a_player_rank_button = Button(self.change_a_player_rank_frame, text='Modify',
                                             command=self.modify_a_player_rank)
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
        player_menu.add_command(label="🔎 Display",
                                command=lambda: ChessMainView.toggle_view(self.player_view, self.tournament_view))
        player_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 Players", menu=player_menu)

        tournament_list_menu = Menu(menu_bar, tearoff=0)
        tournament_list_menu.add_command(label="🔎 Display",
                                         command=lambda: ChessMainView.toggle_view(self.tournament_view,
                                                                                   self.player_view))
        tournament_list_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
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

    def clear_player_view_tree_players_list_selection(self):
        self.player_view.clear_players_list_selection()
