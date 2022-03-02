import string
from random import randint, choice
from tkinter import *
from tkcalendar import Calendar, DateEntry

def google_search():
    webbrowser.open_new('https://www.google.com/search?client=firefox-b-d&q=password+generator')

def generate_password():
    password_min = 8
    password_max = 24
    all_chars = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(all_chars) for x in range(randint(password_min, password_max)))
    champ_password.delete(0, END)
    champ_password.insert(0, password)
    with open('password.txt', 'w+') as file:
        file.write(password+'\n')

def last_passwords():
    with open('password.txt', 'r+') as file:
        title.delete(0, END)
        title.insert(0, file.read())
        file.close()

def display_players ():
    interface = ChessPlayersView()

def modify_rank():
    Input_frame = Frame()
    Input_frame.pack()

    id = Label(Input_frame, text="First Name")
    id.grid(row=0, column=0)

    full_Name = Label(Input_frame, text="Last Name")
    full_Name.grid(row=0, column=1)

    award = Label(Input_frame, text="Rank")
    award.grid(row=0, column=2)

    id_entry = Entry(Input_frame)
    id_entry.grid(row=1, column=0)

    fullname_entry = Entry(Input_frame)
    fullname_entry.grid(row=1, column=1)

    award_entry = Entry(Input_frame)
    award_entry.grid(row=1, column=2)

    buttonApply = Button(Input_frame, text="Apply", fg="red", command=lambda: print('Not implemented'))
    buttonApply.grid(row=2, column=0)

    buttonClose = Button(Input_frame, text="close", fg="red", command=Input_frame.destroy)
    buttonClose.grid(row=2, column=1)

class ChessPlayersTable:

    def __init__(self):
        self.list_widgets = []

    def generate_table_labels(self, frame, row):
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
        player_last_name = Entry(frame)
        player_last_name.insert(0, '')
        player_last_name.grid(row=row, column=0)
        self.list_widgets.append(player_last_name)

        player_first_name = Entry(frame)
        player_first_name.insert(0, '')
        player_first_name.grid(row=row, column=1)
        self.list_widgets.append(player_first_name)

        player_birthdate = DateEntry(frame)
        player_birthdate.grid(row=row, column=2)
        self.list_widgets.append(player_birthdate)

        player_gender = Spinbox(frame, values=('', 'Male', 'Female'))
        player_gender.insert(0, '')
        player_gender.grid(row=row, column=3)
        self.list_widgets.append(player_gender)

        player_rank = Entry(frame)
        player_rank.insert(0, '')
        player_rank.grid(row=row, column=4)
        self.list_widgets.append(player_rank)

        return self.list_widgets



class ChessPlayersView(Frame):

    def __init__(self, height=8, width=5):
        Frame.__init__(self)
        self.numberLines = height
        self.numberColumns = width
        self.pack(fill=Y)
        self.widgets_list = list()
        self.chess_players_table = ChessPlayersTable()

        self.generate_table_actions(self)
        self.chess_players_table.generate_table_labels(self, 0)

        for i in range(self.numberLines):
            self.widgets_list.append(self.chess_players_table.generate_new_player_entry(self, i + 2))

        self.add_table_actions(self.numberLines + 3)

    def generate_table_actions(self, row):
        self.buttonInsert = Button(self, text="Insert", fg="red", command=self.insert)
        self.buttonDisplay = Button(self, text="Display", fg="red", command=self.display)
        self.buttonClose = Button(self, text="close", fg="red", command=self.destroy)

    def add_table_actions(self, row):
        self.buttonInsert.grid(row=row, column=0)
        self.buttonDisplay.grid(row=row, column=1)
        self.buttonClose.grid(row=row, column=2)

    def display(self):
        for i in range(self.numberLines):
            result = ''
            for j in range(self.numberColumns):
                result += ' ' + self.widgets_list[i][j].get()
            print(f'[{i}]={result}')
            #self.results[j].delete(0, END)
            #self.results[j].insert(0, result)


    def insert(self):
        self.numberLines += 1
        self.widgets_list.append(self.chess_players_table.generate_new_player_entry(self, self.numberLines + 2))
        self.add_table_actions(self.numberLines + 3)

class ChessMainView:
    def __init__(self):
        self.main_window = Tk()

        self.main_window.title("Chess Tournaments")
        self.main_window.geometry("720x480")
        self.main_window.minsize(320, 320)
        self.main_window.config(bg="#4065A4")


        #creer une boite
        #frame = Frame(window, bg='#4065A4')

        #creer une sous boite
        #sub_frame = Frame(frame, bg='#4065A4')
        #packer sub_frame
        #sub_frame.grid(row=0, column=1, sticky=W)



        #Affiche la boite
        #frame.pack(expand=YES)

        #Creation d'une barre de menu
        menu_bar = Menu(self.main_window)

        #creer un 1er menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="🔎 search on google", command=google_search)
        file_menu.add_command(label="🗙 Exit", command=self.main_window.quit)
        menu_bar.add_cascade(label="📁 File", menu=file_menu)

        #creer un 2nd menu
        player_report_menu = Menu(tearoff=0)
        player_report_menu.add_command(label="🔎 Alphabetic order", command=lambda: print('Not implemented'))
        player_report_menu.add_command(label="🔎 Ranking order", command=lambda: print('Not implemented'))

        player_menu = Menu(menu_bar, tearoff=0)
        player_menu.add_command(label="🔎 Display", command=display_players)
        player_menu.add_command(label="🔎 Add", command=display_players)
        player_menu.add_command(label="🔎 Modify Rank", command=modify_rank)
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

    def display_interface(self):
        self.main_window.mainloop()
        #self.main_window.destroy()