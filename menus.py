import string
from random import randint, choice
from tkinter import *

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
    interface = IHM(8, 5)

class IHM(Frame):

    ROW_START = 10

    def __init__(self, height, width):
        Frame.__init__(self)
        self.numberLines = height
        self.numberColumns = width
        self.pack(fill=Y)
        self.data = list()
        first_Name = Label(self, text="First Name", bg='Grey', fg='White')
        first_Name.grid(row=self.ROW_START, column=0)
        print(f'top level window title={first_Name.winfo_toplevel().title()}')
        last_Name = Label(self, text="Last Name", bg='Grey', fg='White')
        last_Name.grid(row=self.ROW_START, column=1)
        Birthdate = Label(self, text="Birthdate", bg='Grey', fg='White')
        Birthdate.grid(row=self.ROW_START, column=2)
        Gender = Label(self, text="Gender", bg='Grey', fg='White')
        Gender.grid(row=self.ROW_START, column=3)
        Rank = Label(self, text="Rank", bg='Grey', fg='White')
        Rank.grid(row=self.ROW_START, column=4)

        for i in range(self.numberLines):
            line = list()
            for j in range(self.numberColumns):
                if (j % 3) or (j == 0):
                    cell = Entry(self)
                    cell.insert(0, '')
                    line.append(cell)
                    cell.grid(row=self.ROW_START+i+2, column=j)
                else:
                    spinbox = Spinbox(self, values=('', 'Male', 'Female'))
                    spinbox.insert(0, ' ')
                    line.append(spinbox)
                    spinbox.grid(row=self.ROW_START+i+2, column=j)

            self.data.append(line)

        self.buttonInsert = Button(self, text="Insert", fg="red", command=self.insert)
        self.buttonInsert.grid(row=self.numberLines+self.ROW_START+2, column=0)

        self.buttonDisplay = Button(self, text="Display", fg="red", command=self.display)
        self.buttonDisplay.grid(row=self.numberLines+self.ROW_START+2, column=1)

        self.buttonClose = Button(self, text="close", fg="red", command=self.destroy)
        self.buttonClose.grid(row=self.numberLines+self.ROW_START+2, column=2)

    def display(self):
        for j in range(self.numberColumns):
            result = ''
            for i in range(self.numberLines):
                result += ' ' + self.data[i][j].get()
            print(f'[{i}]={result}')
            #self.results[j].delete(0, END)
            #self.results[j].insert(0, result)


    def insert(self):
        self.numberLines += 1
        line = list()
        for j in range(self.numberColumns):
            cell = Entry(self)
            cell.insert(0, 0)
            line.append(cell)
            cell.grid(row=self.numberLines + self.ROW_START+ 2, column=j)
            self.data.append(line)

        self.buttonInsert.grid(row=self.ROW_START+self.numberLines+3, column=0)
        self.buttonDisplay.grid(row=self.ROW_START+self.numberLines+3, column=1)
        self.buttonClose.grid(row=self.ROW_START+self.numberLines+3, column=2)



#creer une fenetre
window = Tk()

window.title("Password_generator")
window.geometry("720x480")
window.minsize(320, 320)
window.config(bg="#4065A4")


#creer une boite
#frame = Frame(window, bg='#4065A4')

#creer une sous boite
#sub_frame = Frame(frame, bg='#4065A4')
#packer sub_frame
#sub_frame.grid(row=0, column=1, sticky=W)



#Affiche la boite
#frame.pack(expand=YES)

#Creation d'une barre de menu
menu_bar = Menu(window)


#creer un 1er menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="🔎 search on google", command=google_search)
file_menu.add_command(label="🗙 Exit", command=window.quit)
menu_bar.add_cascade(label="📁 File", menu=file_menu)

#creer un 2nd menu
player_menu = Menu(menu_bar, tearoff=0)
player_menu.add_command(label="🔎 Display", command=display_players)
player_menu.add_command(label="🔎 Add", command=display_players)
player_menu.add_command(label="🔎 Modify Rank", command=display_players)
player_menu.add_command(label="🗙 Exit", command=window.quit)
menu_bar.add_cascade(label="📁 Player", menu=player_menu)

#Configurer notre fenetre pour ajouter le menu_bar
window.config(menu=menu_bar)
window.mainloop()
#window.destroy()