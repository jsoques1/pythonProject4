# Program to make a simple
# login screen

import re
import tkinter as tk
from operator import itemgetter
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkinter.messagebox import showerror

main_window = tk.Tk()

# setting the windows size
main_window.geometry("1100x500")
main_window.minsize(1100, 500)

# declaring string variable
last_name_var = tk.StringVar()
first_name_var = tk.StringVar()
birthdate_var = tk.StringVar()
gender_var = tk.StringVar()
rank_var = tk.StringVar()

last_name_var2 = tk.StringVar()
first_name_var2 = tk.StringVar()
birthdate_var2 = tk.StringVar()
gender_var2 = tk.StringVar()
rank_var2 = tk.StringVar()
tree = None


def item_selected(event, tree):
    print(tree.index(tree.selection()))
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        print(item)
        record = item['values']
        print(record)
        # show a message
        last_name_var2.set(record[0])
        first_name_var2.set(record[1])
        birthdate_var2.set(record[2])
        gender_var2.set(record[3])
        rank_var2.set(record[4])
        #showinfo(title='Information', message=','.join(record))

def modify_a_player_rank():
    global tree
    selected = tree.focus()
    temp = tree.item(selected, 'values')
    print(temp)
    print(rank_var2.get())
    print((temp[0], temp[1], temp[2], temp[3], rank_var2.get()))
    if check_int('Rank', rank_var2.get()) is False:
        return False

    tree.item(selected, text='', values=(temp[0], temp[1], temp[2], temp[3], rank_var2.get()))
    last_name_var2.set("")
    first_name_var2.set("")
    birthdate_var2.set("")
    gender_var2.set("")
    rank_var2.set("")
    return True

def sort_tree_column(event, tree):
    values = []
    heading = tree.identify("region", event.x, event.y)
    column = int(tree.identify_column(event.x)[1:])
    if heading == 'heading':
        print('head ' + str(column))
        print(tree.get_children())
        for line in tree.get_children():
            print(tree.item(line))
            print(tree.item(line)['values'][column - 1])
            values.append(tree.item(line)['values'])
        print(f'column = {column}')
        print(f'values = {values}')
        sorted_values = sorted(values, key=itemgetter(column - 1))
        print(f'sorted_values = {sorted_values}')
        tree.delete(*tree.get_children())
        for value in sorted_values:
            player = (value[0], value[1], value[2], value[3], value[4])
            tree.insert('', tk.END, values=player)
    else:
        print('not a head')
        return None


def create_tree_widget(frame):
    style = ttk.Style()
    style.theme_use('clam')
    bg = style.lookup('TFrame', 'background')
    style.configure('Treeview.Heading', background=bg,  font=('calibre', 10, 'bold'))

    columns = ('last name', 'first name', 'birthdate', 'gender', 'rank')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    tree.bind('<Button>', lambda event: sort_tree_column(event, tree))

    # define headings
    tree.heading('last name', text='Last Name')
    tree.heading('first name', text='First Name')
    tree.heading('birthdate', text='Birthdate')
    tree.heading('gender', text='Gender')
    tree.heading('rank', text='Rank')

    tree.bind('<<TreeviewSelect>>', lambda event: item_selected(event, tree))
    tree.grid(row=0, column=0, sticky=NSEW)

    # add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    dummy_players_list = [('a', 'f', '07/03/2022', 'Male', 10),
                          ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          # ('c', 'b', '07/02/2022', 'Female', 1000),
                          ('d', 'a', '07/02/2022', 'Female', 50)
                          ]
    for dummy_player in dummy_players_list:
        tree.insert('', tk.END, values=dummy_player)

    return tree


# def item_selected(self, event):
#    for selected_item in self.tree.selection():
#       item = self.tree.item(selected_item)
#       record = item['values']
#       # show a message
#       showinfo(title='Information', message=','.join(record))

def check_int(name, value):
    if not value.isdigit() or int(value) <= 0 or re.match('^0+\d+$', value) is not None:
        showerror('Error', 'Invalid ' + name)
        return False
    else:
        return True

def check_str(name, value):
    if not isinstance(value, str) or value == '':
        showerror('Error', 'Invalid ' + name)
        return False
    else:
        return True

def check_date(name, value):
    if check_str(name, value) is True:
        if re.match('^\d\d\/\d\d\/\d\d\d\d$', value) is None:
            showerror('Error', 'Invalid ' + name)
            return False
        else:
            return True
    else:
        return False

def check_gender(name, value):
    if check_str(name, value) is True:
        if value not in ['Male', 'Female']:
            showerror('Error', 'Invalid ' + name)
            return False
        else:
            return True
    else:
        return False

def add_a_player():
    global tree
    last_name = last_name_var.get()
    first_name = first_name_var.get()
    birthdate = birthdate_var.get()
    gender = gender_var.get()
    rank = rank_var.get()

    print("The last name is : [" + last_name + ']')
    print("The first name is : [" + first_name + ']')
    print("The birthdate is : [" + birthdate + ']')
    print("The gender is : [" + gender + ']')
    print("The rank is : [" + rank + ']')

    print(type(rank))
    if check_str('Last Name', last_name) is False or \
        check_str('First Name', first_name) is False or \
        check_date('Birthdate', birthdate) is False or \
        check_gender('Gender', gender) is False or \
        check_int('Rank', rank) is False:
        return False

    player = (last_name, first_name, birthdate, gender, rank)
    tree.insert('', tk.END, values=player)
    last_name_var.set("")
    first_name_var.set("")
    birthdate_var.set("")
    gender_var.set("")
    rank_var.set("")
    return True


def show_players_list_frame():
    global tree
    tree_frame = LabelFrame(main_window, text='Players list')
    tree_frame.pack()
    tree = create_tree_widget(tree_frame)


def show_actions_frame():
    action_frame = LabelFrame(main_window, text='Actions')
    action_frame.pack()

    load_btn = Button(action_frame, text='Load', command=lambda: print('Not implemented'))
    load_btn.grid(row=0, column=0, padx=10, pady=10)
    save_btn = Button(action_frame, text='Save', command=lambda: print('Not implemented'))
    save_btn.grid(row=0, column=1, padx=10, pady=10)
    close_btn = Button(action_frame, text='Close', command=lambda: print('Not implemented'))
    close_btn.grid(row=0, column=2, padx=10, pady=10)


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
        gender_entry = Spinbox(frame, values=('', 'Male', 'Female'), textvariable=gender_var, state=widget_state)
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


def show_add_a_player_frame():
    add_a_player_frame = LabelFrame(text='Add a player')
    add_a_player_frame.pack()
    string_var_list = [last_name_var, first_name_var, birthdate_var, gender_var, rank_var]

    fill_a_player_form(add_a_player_frame, string_var_list)
    add_player_button = Button(add_a_player_frame, text='Add', command=add_a_player)
    add_player_button.grid(row=2, column=0)


def show_change_a_player_rank_frame():
    change_a_player_rank_frame = LabelFrame(main_window, text='Modify Rank')
    change_a_player_rank_frame.pack()
    string_var_list = [last_name_var2, first_name_var2, birthdate_var2, gender_var2, rank_var2]
    fill_a_player_form(change_a_player_rank_frame, string_var_list, widget_state=DISABLED)
    change_a_player_rank_button = Button(change_a_player_rank_frame, text='Modify', command=modify_a_player_rank)
    change_a_player_rank_button.grid(row=2, column=0)


show_players_list_frame()
show_actions_frame()
show_add_a_player_frame()
show_change_a_player_rank_frame()

main_window.mainloop()
