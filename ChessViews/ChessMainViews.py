from operator import itemgetter
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from ChessUtils import ChessUtils


class ChessPlayersView:
    def __init__(self, controller, numberLines=9, numberColumns=5):
        self.my_controller = controller
        self.numberLines = numberLines
        self.numberColumns = numberColumns
        self.is_built = False

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

    # def add_a_vertical_scrollbar(self):
    #     canvas = Canvas(self, borderwidth=0, background="#ffffff")
    #     canvas.pack(side=LEFT, fill=BOTH, expand=True)
    #
    #     verticalScrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
    #     verticalScrollbar.pack(side=RIGHT, fill='y')
    #
    #     canvas.configure(yscrollcommand=verticalScrollbar.set)
    #     # canvas.pack()
    #     canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox('all')))
    #
    #     self.myFrame = Frame(canvas)
    #     # myFrame.pack()
    #
    #     canvas.create_window((0,0), window=self.myFrame, anchor="nw")
    #
    #     self.pack(fill="both",  expand=True, padx=10, pady=10)
    #
    #     # for i in range(50):
    #     #     myButton = Button(self.myFrame, text='my Button - ' + str(i))
    #     #     # myButton.grid(i, 0)
    #     #     myButton.pack()
    #
    #     # canvas.create_window((4, 4), window=self, anchor="nw")
    #     # self.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    #
    # def select_player_entry(self, event, row):
    #     self.current_entry_row = row
    #     print(row)
    #
    # def generate_new_player_entry(self, row):
    #     players_widgets_list = []
    #
    #     player_last_name = Entry(self.myFrame, textvariable=StringVar())
    #     player_last_name.insert(0, '')
    #     player_last_name.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
    #     player_last_name.grid(row=row, column=0)
    #     players_widgets_list.append(player_last_name)
    #
    #     player_first_name = Entry(self.myFrame, textvariable=StringVar())
    #     player_first_name.insert(0, '')
    #     player_first_name.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
    #     player_first_name.grid(row=row, column=1)
    #     players_widgets_list.append(player_first_name)
    #
    #     player_birthdate = DateEntry(self.myFrame, textvariable=StringVar(), date_pattern='dd/mm/yyyy')
    #     player_birthdate.insert(0, '')
    #     player_birthdate.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
    #     player_birthdate.grid(row=row, column=2)
    #     players_widgets_list.append(player_birthdate)
    #
    #     player_gender = Spinbox(self.myFrame, values=('', 'Male', 'Female'), textvariable=StringVar())
    #     player_gender.insert(0, '')
    #     player_gender.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
    #     player_gender.grid(row=row, column=3)
    #     players_widgets_list.append(player_gender)
    #
    #     player_rank = Entry(self.myFrame, textvariable=StringVar())
    #     player_rank.insert(0, '')
    #     player_rank.bind("<Button>", lambda event, row=row: self.select_player_entry(event, row))
    #     player_rank.grid(row=row, column=4)
    #     players_widgets_list.append(player_rank)
    #
    #     return players_widgets_list
    #
    # def generate_player_labels_view(self):
    #     last_name = Label(self.myFrame, text="Last Name", bg='Grey', fg='White')
    #     last_name.grid(row=0, column=0)
    #     last_name.bind("<Button>", lambda event: self.sort_players_list_by_name())
    #     first_name = Label(self.myFrame, text="First Name", bg='Grey', fg='White')
    #     first_name.grid(row=0, column=1)
    #     birthdate = Label(self.myFrame, text="Birthdate", bg='Grey', fg='White')
    #     birthdate.grid(row=0, column=2)
    #     gender = Label(self.myFrame, text="Gender", bg='Grey', fg='White')
    #     gender.grid(row=0, column=3)
    #     rank = Label(self.myFrame, text="Rank", bg='Grey', fg='White')
    #     rank.grid(row=0, column=4)
    #     rank.bind("<Button>", lambda event: self.sort_players_list_by_rank())
    #
    # def make_players_list_from_widgets(self):
    #     players_list = []
    #     for i in range(int(self.numberLines)):
    #         player = []
    #         for j in range(int(self.numberColumns)):
    #             player.append(self.players_widgets_list[i][j].get())
    #         players_list.append(player)
    #     return players_list
    #
    # def clean_players_list(self):
    #     players_list = []
    #     for i in range(int(self.numberLines)):
    #         player = []
    #         for j in range(int(self.numberColumns)):
    #             player.append(self.players_widgets_list[i][j].get())
    #         players_list.append(player)
    #     return players_list
    #
    # def fill_players_widgets_list(self, sorted_players_list):
    #     for i in range(int(self.numberLines)):
    #         for j in range(int(self.numberColumns)):
    #             self.players_widgets_list[i][j].delete(0, END)
    #             self.players_widgets_list[i][j].insert(0, sorted_players_list[i][j])
    #
    # def sort_players_list_by_name(self):
    #     logging.debug('sort_players_list_by_name')
    #     players_list = self.make_players_list_from_widgets()
    #     sorted_players_list = self.my_controller.sort_players_list_by_name(players_list)
    #     self.fill_players_widgets_list(sorted_players_list)
    #
    # def sort_players_list_by_rank(self):
    #     logging.debug('sort_players_list_by_rank')
    #     players_list = self.make_players_list_from_widgets()
    #     sorted_players_list = self.my_controller.sort_players_list_by_rank(players_list)
    #     self.fill_players_widgets_list(sorted_players_list)
    #
    # def make_chess_players_view(self):
    #     self.generate_player_labels_view()
    #     self.generate_players_entry_view()
    #     self.generate_players_actions_view()
    #
    # def generate_players_entry_view(self):
    #     for i in range(int(self.numberLines)):
    #         self.players_widgets_list.append(self.generate_new_player_entry(i + 2))
    #
    # def clear_player(self):
    #     if self.current_entry_row is not None:
    #         print(f'{len(self.players_widgets_list)} {self.numberLines}')
    #         for i in range(int(self.numberColumns)):
    #             self.players_widgets_list[self.current_entry_row - 2][i].delete(0, END)
    #         self.current_entry_row = None
    #
    # def generate_players_actions_view(self):
    #     self.button_add = Button(self.myFrame, text="Add", fg="red", command=self.add_player)
    #     self.button_load = Button(self.myFrame, text="Load", fg="red", command=self.load_players_list)
    #     self.button_save = Button(self.myFrame, text="Save", fg="red", command=self.save_players_list)
    #     self.button_clear = Button(self.myFrame, text="Clear", fg="red", command=self.clear_player)
    #     self.button_close = Button(self.myFrame, text="Close", fg="red", command=self.close_players_list_frame)
    #     self.add_table_actions_view()
    #
    # def add_table_actions_view(self):
    #     self.button_add.grid(row=self.numberLines + 3, column=0)
    #     self.button_load.grid(row=self.numberLines + 3, column=1)
    #     self.button_save.grid(row=self.numberLines + 3, column=2)
    #     self.button_clear.grid(row=self.numberLines + 3, column=3)
    #     self.button_close.grid(row=self.numberLines + 3, column=4)
    #
    # def add_player(self):
    #     self.numberLines += 1
    #     logging.debug(f'add_player({self.numberLines + 1})')
    #     self.players_widgets_list.append(self.generate_new_player_entry(self.numberLines + 1))
    #     self.add_table_actions_view()
    #
    # def save_players_list(self):
    #     logging.debug('save_players_list')
    #     players_list = []
    #     for i in range(int(self.numberLines)):
    #         player = []
    #         for j in range(int(self.numberColumns)):
    #             player.append(self.players_widgets_list[i][j].get())
    #         players_list.append(player)
    #     logging.info(f'players_list={players_list}')
    #     result = self.my_controller.save_players_list(players_list)
    #
    # def load_players_list(self):
    #     logging.debug('load_players_list')
    #     players_list = self.my_controller.load_players_list()
    #     logging.info(f'{len(players_list)} players={players_list}')
    #     if len(players_list) != 0:
    #         lines_to_add = len(players_list) - int(self.numberLines)
    #         for i in range(lines_to_add):
    #             self.add_player()
    #         self.add_table_actions_view()
    #
    #         for i in range(int(self.numberLines)):
    #             for j in range(int(self.numberColumns)):
    #                 self.players_widgets_list[i][j].delete(0, END)
    #                 self.players_widgets_list[i][j].insert(0, players_list[i][j])
    #
    # def display_players(self):
    #     if self.is_built is False:
    #         self.add_a_vertical_scrollbar()
    #         self.make_chess_players_view()
    #         self.load_players_list()
    #         self.is_built = True
    #     else:
    #         self.open_players_list_frame()
    #
    # # def players_list_sort_decorator(self, fonction):
    # #     def wrapper(self):
    # #         logging.debug('players_list_sort_decorator')
    # #         players_list = []
    # #         for i in range(int(self.numberLines)):
    # #             player = []
    # #             for j in range(int(self.numberColumns)):
    # #             player.append(self.players_widgets_list[i][j].get())
    # #             players_list.append(player)
    # #
    # #             sorted_players_list = self.fonction(players_list)
    # #
    # #             for i in range(int(self.numberLines)):
    # #                 for j in range(int(self.numberColumns)):
    # #                     self.players_widgets_list[i][j].delete(0, END)
    # #                     self.players_widgets_list[i][j].insert(0, sorted_players_list[i][j])
    # #         return wrapper
    #
    # def set_my_controller(self, controller):
    #     self.my_controller = controller
    #
    # def open_players_list_frame(self):
    #     logging.debug('open_players_list_frame')
    #     self.pack(fill="both", expand=True)
    #
    # def close_players_list_frame(self):
    #     logging.debug('close_players_list_frame')
    #     self.pack_forget()

    def set_my_controller(self, controller):
        self.my_controller = controller

    def item_selected(self, event, tree):
        print(self.tree.index(self.tree.selection()))
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            print(item)
            record = item['values']
            print(record)
            # show a message
            self.last_name_var2.set(record[0])
            self.first_name_var2.set(record[1])
            self.birthdate_var2.set(record[2])
            self.gender_var2.set(record[3])
            self.rank_var2.set(record[4])


    def modify_a_player_rank(self):
        print('modify_a_player_rank')
        selected = self.tree.focus()
        temp = self.tree.item(selected, 'values')
        print(temp)
        print(self.rank_var2.get())
        print((temp[0], temp[1], temp[2], temp[3], self.rank_var2.get(), temp[5]))
        if ChessUtils.check_int('Rank', self.rank_var2.get()) is False:
            return False
        player = (temp[0], temp[1], temp[2], temp[3], self.rank_var2.get(), temp[5])
        self.my_controller.update_a_player_rank(player, self.rank_var2.get())
        self.tree.item(selected, text='', values=player)
        self.last_name_var2.set("")
        self.first_name_var2.set("")
        self.birthdate_var2.set("")
        self.gender_var2.set("")
        self.rank_var2.set("")
        return True

    def sort_tree_column(self, event):
        values = []
        heading = self.tree.identify("region", event.x, event.y)
        column = int(self.tree.identify_column(event.x)[1:])
        if heading == 'heading':
            print('head ' + str(column))
            print(self.tree.get_children())
            for line in self.tree.get_children():
                print(self.tree.item(line))
                print(self.tree.item(line)['values'][column - 1])
                values.append(self.tree.item(line)['values'])
            print(f'column = {column}')
            print(f'values = {values}')
            sorted_values = sorted(values, key=itemgetter(column - 1))
            print(f'sorted_values = {sorted_values}')
            self.tree.delete(*self.tree.get_children())
            for value in sorted_values:
                player = (value[0], value[1], value[2], value[3], value[4], value[5])
                self.tree.insert('', END, values=player)
        else:
            print('not a head')
            return None

    def get_player_id(self):
        self.player_id += 1
        return self.player_id

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

    # def item_selected(self, event):
    #    for selected_item in self.tree.selection():
    #       item = self.tree.item(selected_item)
    #       record = item['values']
    #       # show a message
    #       showinfo(title='Information', message=','.join(record))


    def add_a_player(self):
        last_name = self.last_name_var.get()
        first_name = self.first_name_var.get()
        birthdate = self.birthdate_var.get()
        gender = self.gender_var.get()
        rank = self.rank_var.get()

        print("The last name is : [" + last_name + ']')
        print("The first name is : [" + first_name + ']')
        print("The birthdate is : [" + birthdate + ']')
        print("The gender is : [" + gender + ']')
        print("The rank is : [" + rank + ']')

        if ChessUtils.check_str('Last Name', last_name) is False or \
            ChessUtils.check_str('First Name', first_name) is False or \
            ChessUtils.check_date('Birthdate', birthdate) is False or \
            ChessUtils.check_gender('Gender', gender) is False or \
            ChessUtils.check_int('Rank', rank) is False:
            return False

        player = (last_name, first_name, birthdate, gender, rank, self.get_player_id())
        print(player)
        self.my_controller.save_a_player(player)

        self.tree.insert('', END, values=player)
        self.last_name_var.set("")
        self.first_name_var.set("")
        self.birthdate_var.set("")
        self.gender_var.set("")
        self.rank_var.set("")
        return True


    def show_players_list_frame(self):
        self.tree_frame = LabelFrame(self.main_window, text='Players list')
        self.tree_frame.pack()
        self.create_tree_widget(self.tree_frame)


    def show_actions_frame(self):
        self.action_frame = LabelFrame(self.main_window, text='Actions')
        self.action_frame.pack()

        load_btn = Button(self.action_frame, text='Load', command=lambda: print('Not implemented'))
        load_btn.grid(row=0, column=0, padx=10, pady=10)
        save_btn = Button(self.action_frame, text='Save', command=lambda: print('Not implemented'))
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
            print('create all frame')
            self.show_players_list_frame()
            self.show_actions_frame()
            self.show_change_a_player_rank_frame()
            self.show_add_a_player_frame()
            self.is_already_created = True
        else:
            print('reopen all frame')
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
