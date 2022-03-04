import logging
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry


def display_players(my_controller):
    view = ChessPlayersView()
    view.set_my_controller(my_controller)
    view.add_a_vertical_scrollbar()
    view.make_chess_players_view()
    view.load_players_list()

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

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


class ChessPlayersView(LabelFrame):
    def __init__(self, numberLines=9, numberColumns=5):
        LabelFrame.__init__(self, text='Players List')
        self.my_controller = None
        self.numberLines = numberLines
        self.numberColumns = numberColumns
        #self.pack(fill=Y)

        self.players_widgets_list = list()
        self.button_add = None
        self.button_load = None
        self.button_save = None
        self.button_clear = None
        self.button_close = None
        self.current_entry_row = None

        self.myFrame = None

    def add_a_vertical_scrollbar(self):
        canvas = Canvas(self, borderwidth=0, background="#ffffff")
        canvas.pack(side=LEFT, fill=BOTH, expand="yes")

        verticalScrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        verticalScrollbar.pack(side=RIGHT, fill='y')

        canvas.configure(yscrollcommand=verticalScrollbar.set)
        # canvas.pack()
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox('all')))

        self.myFrame = Frame(canvas)
        # myFrame.pack()

        canvas.create_window((0,0), window=self.myFrame, anchor="nw")

        self.pack(fill="both",  expand="yes", padx=10, pady=10)

        # for i in range(50):
        #     myButton = Button(self.myFrame, text='my Button - ' + str(i))
        #     # myButton.grid(i, 0)
        #     myButton.pack()

        # canvas.create_window((4, 4), window=self, anchor="nw")
        # self.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    def select_player_entry(self, event, row):
        self.current_entry_row = row
        print(row)

    def generate_new_player_entry(self, row):
        players_widgets_list = []

        player_last_name = Entry(self.myFrame, textvariable=StringVar())
        player_last_name.insert(0, '')
        player_last_name.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
        player_last_name.grid(row=row, column=0)
        players_widgets_list.append(player_last_name)

        player_first_name = Entry(self.myFrame, textvariable=StringVar())
        player_first_name.insert(0, '')
        player_first_name.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
        player_first_name.grid(row=row, column=1)
        players_widgets_list.append(player_first_name)

        player_birthdate = DateEntry(self.myFrame, textvariable=StringVar(), date_pattern='dd/mm/yyyy')
        player_birthdate.insert(0, '')
        player_birthdate.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
        player_birthdate.grid(row=row, column=2)
        players_widgets_list.append(player_birthdate)

        player_gender = Spinbox(self.myFrame, values=('', 'Male', 'Female'), textvariable=StringVar())
        player_gender.insert(0, '')
        player_gender.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
        player_gender.grid(row=row, column=3)
        players_widgets_list.append(player_gender)

        player_rank = Entry(self.myFrame, textvariable=StringVar())
        player_rank.insert(0, '')
        player_rank.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
        player_rank.grid(row=row, column=4)
        players_widgets_list.append(player_rank)

        return players_widgets_list

    def generate_player_labels_view(self):
        last_name = Label(self.myFrame, text="Last Name", bg='Grey', fg='White')
        last_name.grid(row=0, column=0)
        last_name.bind("<Button>", lambda event: self.sort_players_list_by_name())
        first_name = Label(self.myFrame, text="First Name", bg='Grey', fg='White')
        first_name.grid(row=0, column=1)
        birthdate = Label(self.myFrame, text="Birthdate", bg='Grey', fg='White')
        birthdate.grid(row=0, column=2)
        gender = Label(self.myFrame, text="Gender", bg='Grey', fg='White')
        gender.grid(row=0, column=3)
        rank = Label(self.myFrame, text="Rank", bg='Grey', fg='White')
        rank.grid(row=0, column=4)
        rank.bind("<Button>", lambda event: self.sort_players_list_by_rank())

    def sort_players_list_by_name(self):
        logging.debug('sort_players_list_by_name')
        players_list = []
        for i in range(int(self.numberLines)):
            player = []
            for j in range(int(self.numberColumns)):
                player.append(self.players_widgets_list[i][j].get())
            players_list.append(player)

        sorted_players_list = self.my_controller.sort_players_list_by_name(players_list)

        for i in range(int(self.numberLines)):
            for j in range(int(self.numberColumns)):
                self.players_widgets_list[i][j].delete(0, END)
                self.players_widgets_list[i][j].insert(0, sorted_players_list[i][j])

    def sort_players_list_by_rank(self):
        logging.debug('sort_players_list_by_rank')
        players_list = []
        for i in range(int(self.numberLines)):
            player = []
            for j in range(int(self.numberColumns)):
                player.append(self.players_widgets_list[i][j].get())
            players_list.append(player)

        sorted_players_list = self.my_controller.sort_players_list_by_rank(players_list)

        for i in range(int(self.numberLines)):
            for j in range(int(self.numberColumns)):
                self.players_widgets_list[i][j].delete(0, END)
                self.players_widgets_list[i][j].insert(0, sorted_players_list[i][j])

    def make_chess_players_view(self):
        self.generate_player_labels_view()
        self.generate_players_entry_view()
        self.generate_players_actions_view()
 
    def generate_players_entry_view(self):
        for i in range(int(self.numberLines)):
            self.players_widgets_list.append(self.generate_new_player_entry(i + 2))

    def clear_player(self):
        if self.current_entry_row is not None:
            print(f'{len(self.players_widgets_list)} {self.numberLines}')
            for i in range(int(self.numberColumns)):
                self.players_widgets_list[self.current_entry_row - 2][i].delete(0, END)
            self.current_entry_row = None

    def generate_players_actions_view(self):
        self.button_add = Button(self.myFrame, text="Add", fg="red", command=self.add_player)
        self.button_load = Button(self.myFrame, text="Load", fg="red", command=self.load_players_list)
        self.button_save = Button(self.myFrame, text="Save", fg="red", command=self.save_players_list)
        self.button_clear = Button(self.myFrame, text="Clear", fg="red", command=self.clear_player)
        self.button_close = Button(self.myFrame, text="Close", fg="red", command=self.close_players_list_frame)
        self.add_table_actions_view()
        
    def add_table_actions_view(self):
        self.button_add.grid(row=self.numberLines + 3, column=0)
        self.button_load.grid(row=self.numberLines + 3, column=1)
        self.button_save.grid(row=self.numberLines + 3, column=2)
        self.button_clear.grid(row=self.numberLines + 3, column=3)
        self.button_close.grid(row=self.numberLines + 3, column=4)

    def add_player(self):
        self.numberLines += 1
        logging.debug(f'add_player({self.numberLines + 1})')
        self.players_widgets_list.append(self.generate_new_player_entry(self.numberLines + 1))
        self.add_table_actions_view()

    def save_players_list(self):
        logging.debug('save_players_list')
        players_list = []
        for i in range(int(self.numberLines)):
            player = []
            for j in range(int(self.numberColumns)):
                player.append(self.players_widgets_list[i][j].get())
            players_list.append(player)
        logging.info(f'players_list={players_list}')
        result = self.my_controller.save_players_list(players_list)

    def load_players_list(self):
        logging.debug('load_players_list')
        players_list = self.my_controller.load_players_list()
        logging.info(f'{len(players_list)} players={players_list}')
        if len(players_list) != 0:
            lines_to_add = len(players_list) - int(self.numberLines)
            for i in range(lines_to_add):
                self.add_player()
            self.add_table_actions_view()

            for i in range(int(self.numberLines)):
                for j in range(int(self.numberColumns)):
                    self.players_widgets_list[i][j].delete(0, END)
                    self.players_widgets_list[i][j].insert(0, players_list[i][j])

    # def players_list_sort_decorator(self, fonction):
    #     def wrapper(self):
    #         logging.debug('players_list_sort_decorator')
    #         players_list = []
    #         for i in range(int(self.numberLines)):
    #             player = []
    #             for j in range(int(self.numberColumns)):
    #             player.append(self.players_widgets_list[i][j].get())
    #             players_list.append(player)
    #
    #             sorted_players_list = self.fonction(players_list)
    #
    #             for i in range(int(self.numberLines)):
    #                 for j in range(int(self.numberColumns)):
    #                     self.players_widgets_list[i][j].delete(0, END)
    #                     self.players_widgets_list[i][j].insert(0, sorted_players_list[i][j])
    #         return wrapper



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
        # self.main_window.geometry("500x500")
        self.main_window.minsize(320, 320)
        self.main_window.config(bg='Blue')
        # self.main_window.resizable(False, False)

        self.list_frame = LabelFrame(self.main_window, bg='Blue')
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
        player_menu = Menu(menu_bar, tearoff=0)
        player_menu.add_command(label="🔎 Display", command=lambda: display_players(self.my_controller))
        player_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 Players", menu=player_menu)

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
        menu_bar.add_cascade(label="📁 Tournaments", menu=tournament_menu)

        #Configurer notre fenetre pour ajouter le menu_bar
        self.main_window.config(menu=menu_bar)

        self.player_view = ChessPlayersView(self.my_controller)

    def set_my_controller(self, controller):
        self.my_controller = controller

    def display_interface(self):
        self.main_window.mainloop()
        #self.main_window.destroy()
