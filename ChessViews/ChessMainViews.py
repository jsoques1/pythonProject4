import configparser
import logging
from operator import itemgetter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from ChessUtils import ChessUtils


class ChessPlayersView:
    def __init__(self, controller):
        self.my_controller = controller
        self.is_built = False
        self.is_debug = None

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

        self.tree = None
        self.is_already_created = False
        self.player_id = 0

        self.main_window = None
        self.tree_frame = None
        self.action_frame = None
        self.add_a_player_frame = None
        self.change_a_player_rank_frame = None

        self.is_debug = ChessPlayersView.read_views_section_config_file()


    def set_my_controller(self, controller):
        self.my_controller = controller

    def item_selected(self, event, tree):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            player = item['values']
            # show a message
            self.last_name_var2.set(player[0])
            self.first_name_var2.set(player[1])
            self.birthdate_var2.set(player[2])
            self.gender_var2.set(player[3])
            self.rank_var2.set(player[4])

    def clear_players_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_players_list_in_view(self):
        logging.debug('load_players_list_in_view')
        self.clear_players_list()
        players_list = self.my_controller.load_players_list()
        logging.info(players_list)
        for player in players_list:
            self.tree.insert('', END, values=player)
        self.set_player_id(len(players_list))

    def modify_a_player_rank(self):
        logging.debug('modify_a_player_rank')
        selected = self.tree.focus()
        if ChessUtils.check_int('Rank', self.rank_var2.get()) is False:
            return False
        values = self.tree.item(selected, 'values')
        player = (values[0], values[1], values[2], values[3], self.rank_var2.get(), values[5])
        logging.info(f'{player}')
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
            ChessUtils.check_gender('Gender', gender) is False or \
            ChessUtils.check_int('Rank', rank) is False:
            return False

        player = (last_name, first_name, birthdate, gender, rank, self.get_player_id())
        logging.debug(f'add a player {player}')
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

    def set_player_id(self, player_id):
        self.player_id = player_id
        return self.player_id

    def get_player_id(self):
        self.player_id += 1
        return self.player_id

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
            dummy_players_list = [('Messi', 'Lionel', '07/03/1984', 'Male', 1000, self.get_player_id()),
                                  ('Bronze', 'Lucy', '07/02/1990', 'Female', 2000, self.get_player_id()),
                                  ('Greenwood', 'Alex', '07/02/1996', 'Female', 1000, self.get_player_id()),
                                  ('Hegerberg', 'Ada', '07/02/1998', 'Female', 1000, self.get_player_id()),
                                  ('Ronaldo', 'Cristiano', '07/02/1990', 'Male', 4000, self.get_player_id()),
                                  ('Loris', 'Hugo', '07/02/1997', 'Male', 3000, self.get_player_id()),
                                  ('Weir', 'Stephanie', '07/02/2000', 'Female', 1000, self.get_player_id()),
                                  ('Bouhaddi', 'Sarah', '07/02/1986', 'Female', 5000, self.get_player_id())
                                  ]

            self.my_controller.save_players_list(dummy_players_list)

            for dummy_player in dummy_players_list:
                self.tree.insert('', END, values=dummy_player)
        else:
            self.load_players_list_in_view()

    @staticmethod
    def read_views_section_config_file():
        logging.debug('read_views_section_config_file')
        config = configparser.ConfigParser()
        config.read('MyChessApp.ini')
        is_debug = config['views']['is_debug']
        return is_debug

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

    def hide_all(self):
        if self.is_already_created is True:
            self.tree_frame.pack_forget()
            self.action_frame.pack_forget()
            self.change_a_player_rank_frame.pack_forget()
            self.add_a_player_frame.pack_forget()


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

        self.main_window = Tk()

        self.main_window.title("Chess Tournaments")
        self.main_window.geometry("1100x500")
        self.main_window.minsize(1100, 500)

        self.is_debug = ChessPlayersView.read_views_section_config_file()

        # Creation d'une barre de menu
        menu_bar = Menu(self.main_window)

        #creer un 1er menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 File", menu=file_menu)

        #creer un 2nd menu
        player_menu = Menu(menu_bar, tearoff=0)
        player_menu.add_command(label="🔎 Display", command=lambda: self.player_view.show_all())
        player_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 Players", menu=player_menu)

        #creer un 3eme menu
        tournament_list_menu = Menu(tearoff=0)
        tournament_list_menu.add_command(label="🔎 Display", command=lambda: print('Not implemented'))

        tournament_menu = Menu(menu_bar, tearoff=0)
        tournament_menu.add_command(label="🔎 Create", command=lambda: print('Not implemented'))
        tournament_menu.add_command(label="🔎 Start", command=lambda: print('Not implemented'))
        tournament_menu.add_command(label="🔎 Suspend", command=lambda: print('Not implemented'))
        tournament_menu.add_command(label="🔎 Resume", command=lambda: print('Not implemented'))
        tournament_menu.add_command(label="🔎 Cancel", command=lambda: print('Not implemented'))
        tournament_menu.add_cascade(label="🔎 List", menu=tournament_list_menu)
        tournament_menu.add_command(label="🗙 Exit", command=lambda: print('Not implemented'))
        menu_bar.add_cascade(label="📁 Tournaments", menu=tournament_menu)

        #Configurer notre fenetre pour ajouter le menu_bar
        self.main_window.config(menu=menu_bar)



    def set_my_controller(self, controller):
        self.my_controller = controller
        self.player_view = ChessPlayersView(controller)

    def display_interface(self):
        self.main_window.mainloop()
        #self.main_window.destroy()
