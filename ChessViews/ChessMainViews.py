import logging
from tkinter import *
from tkcalendar import Calendar, DateEntry


def display_players(my_controller):
    view = ChessPlayersView()
    view.set_my_controller(my_controller)
    view.make_chess_players_table()
    view.load_players_list()


def modify_rank():
    input_frame = Frame()
    input_frame.pack()

    first_name = Label(input_frame, text="First Name")
    first_name.grid(row=0, column=0)

    full_name = Label(input_frame, text="Last Name")
    full_name.grid(row=0, column=1)

    rank = Label(input_frame, text="Rank")
    rank.grid(row=0, column=2)

    id_entry = Entry(input_frame)
    id_entry.grid(row=1, column=0)

    fullname_entry = Entry(input_frame)
    fullname_entry.grid(row=1, column=1)

    award_entry = Entry(input_frame)
    award_entry.grid(row=1, column=2)

    button_apply = Button(input_frame, text="Apply", fg="red", command=lambda: print('Not implemented'))
    button_apply.grid(row=2, column=0)

    button_close = Button(input_frame, text="close", fg="red", command=input_frame.destroy)
    button_close.grid(row=2, column=1)


class ChessPlayersTable:
    def __init__(self):
        pass

    def generate_table_labels(self, frame):
        last_name = Label(frame, text="Last Name", bg='Grey', fg='White')
        last_name.grid(row=0, column=0)
        first_name = Label(frame, text="First Name", bg='Grey', fg='White')
        first_name.grid(row=0, column=1)
        birthdate = Label(frame, text="Birthdate", bg='Grey', fg='White')
        birthdate.grid(row=0, column=2)
        gender = Label(frame, text="Gender", bg='Grey', fg='White')
        gender.grid(row=0, column=3)
        rank = Label(frame, text="Rank", bg='Grey', fg='White')
        rank.grid(row=0, column=4)

    def generate_new_player_entry(self, frame, row):
        widgets_list = []

        player_last_name = Entry(frame, textvariable=StringVar())
        player_last_name.insert(0, '')
        player_last_name.grid(row=row, column=0)
        widgets_list.append(player_last_name)

        player_first_name = Entry(frame, textvariable=StringVar())
        player_first_name.insert(0, '')
        player_first_name.grid(row=row, column=1)
        widgets_list.append(player_first_name)

        player_birthdate = DateEntry(frame, textvariable=StringVar())
        player_birthdate.grid(row=row, column=2)
        widgets_list.append(player_birthdate)

        player_gender = Spinbox(frame, values=('', 'Male', 'Female'), textvariable=StringVar())
        player_gender.insert(0, '')
        player_gender.grid(row=row, column=3)
        widgets_list.append(player_gender)

        player_rank = Entry(frame, textvariable=StringVar())
        player_rank.insert(0, '')
        player_rank.grid(row=row, column=4)
        widgets_list.append(player_rank)

        return widgets_list


class ChessPlayersView(Frame):
    def __init__(self, height=8, width=5):
        Frame.__init__(self)
        self.my_controller = None

        self.numberLines = height
        self.numberColumns = width
        self.pack(fill=Y)

        self.widgets_list = list()
        self.chess_players_table = None
        self.button_add = None
        self.button_load = None
        self.button_save = None
        self.button_close = None

    def make_chess_players_table(self):
        self.chess_players_table = ChessPlayersTable()
        self.generate_table_actions()
        self.chess_players_table.generate_table_labels(self)

        for i in range(int(self.numberLines)):
            self.widgets_list.append(self.chess_players_table.generate_new_player_entry(self, i + 2))

        self.add_table_actions(self.numberLines + 3)

    def generate_table_actions(self):
        self.button_add = Button(self, text="Add", fg="red", command=self.add_player)
        self.button_load = Button(self, text="Load", fg="red", command=self.load_players_list)
        self.button_save = Button(self, text="Save", fg="red", command=self.save_players_list)
        self.button_close = Button(self, text="Close", fg="red", command=self.close_players_list_frame)

    def add_table_actions(self, row):
        self.button_add.grid(row=row, column=0)
        self.button_load.grid(row=row, column=1)
        self.button_save.grid(row=row, column=2)
        self.button_close.grid(row=row, column=3)

    def add_player(self):
        self.numberLines += 1
        self.widgets_list.append(self.chess_players_table.generate_new_player_entry(self, self.numberLines + 2))
        self.add_table_actions(self.numberLines + 3)

    def save_players_list(self):
        logging.debug('save_players_list')
        players_list = []
        for i in range(int(self.numberLines)):
            player = []
            for j in range(int(self.numberColumns)):
                player.append(self.widgets_list[i][j].get())
            players_list.append(player)
        logging.info(f'players_list={players_list}')
        result = self.my_controller.save_players_list(players_list)

    def load_players_list(self):
        logging.debug('load_players_list')
        players_list = self.my_controller.load_players_list()
        logging.info(f'{len(players_list)} players={players_list}')
        lines_to_add = len(players_list) - int(self.numberLines)
        for i in range(lines_to_add):
            self.add_player()
        self.add_table_actions(self.numberLines + 3)

        for i in range(int(self.numberLines)):
            for j in range(int(self.numberColumns)):
                self.widgets_list[i][j].delete(0, END)
                self.widgets_list[i][j].insert(0, players_list[i][j])

    def set_my_controller(self, controller):
        self.my_controller = controller

    def close_players_list_frame(self):
        self.destroy()


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
        self.main_window.geometry("720x480")
        self.main_window.minsize(320, 320)
        self.main_window.config(bg="#4065A4")

        self.list_frame = LabelFrame(self.main_window, bg='#4065A4')
        self.message_frame = LabelFrame(self.main_window, bg='grey')

        self.list_frame.pack(side=TOP)
        self.message_frame.pack(side=BOTTOM)

        Label(self.list_frame, text="Frame 1").pack(padx=10, pady=10)
        Label(self.message_frame, text="Frame 2").pack(padx=10, pady=10)

        #sub_frame = Frame(frame, bg='#4065A4')
        #packer sub_frame
        #sub_frame.grid(row=0, column=1, sticky=W)

        #Affiche la boite
        #frame.pack(expand=YES)

        # Creation d'une barre de menu
        menu_bar = Menu(self.main_window)

        #creer un 1er menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 File", menu=file_menu)

        #creer un 2nd menu
        player_report_menu = Menu(tearoff=0)
        player_report_menu.add_command(label="🔎 Alphabetic order", command=lambda: print('Not implemented'))
        player_report_menu.add_command(label="🔎 Ranking order", command=lambda: print('Not implemented'))

        player_menu = Menu(menu_bar, tearoff=0)
        player_menu.add_command(label="🔎 Display", command=lambda: display_players(self.my_controller))
        #player_menu.add_command(label="🔎 Modify Rank", command=modify_rank)
        player_menu.add_cascade(label="🔎 Report", menu=player_report_menu)
        player_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 Player", menu=player_menu)

        #creer un 3eme menu
        tournament_list_menu = Menu(tearoff=0)
        tournament_list_menu.add_command(label="🔎 All", command=lambda: print('Not implemented'))
        tournament_list_menu.add_command(label="🔎 Single", command=lambda: print('Not implemented'))

        tournament_menu = Menu(menu_bar, tearoff=0)
        tournament_menu.add_command(label="🔎 Create", command=lambda: print('Not implemented'))
        tournament_menu.add_command(label="🔎 Start", command=lambda: print('Not implemented'))
        tournament_menu.add_command(label="🔎 Suspend", command=lambda: print('Not implemented'))
        tournament_menu.add_command(label="🔎 Resume", command=lambda: print('Not implemented'))
        tournament_menu.add_command(label="🔎 Cancel", command=lambda: print('Not implemented'))
        tournament_menu.add_cascade(label="🔎 List", menu=tournament_list_menu)
        tournament_menu.add_command(label="🗙 Exit", command=lambda: print('Not implemented'))
        menu_bar.add_cascade(label="📁 Tournament", menu=tournament_menu)

        #Configurer notre fenetre pour ajouter le menu_bar
        self.main_window.config(menu=menu_bar)

        self.player_view = ChessPlayersView(self.my_controller)

    def set_my_controller(self, controller):
        self.my_controller = controller

    def display_interface(self):
        self.main_window.mainloop()
        #self.main_window.destroy()
