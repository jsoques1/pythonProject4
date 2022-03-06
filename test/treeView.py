# Program to make a simple
# login screen


import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkinter.messagebox import showinfo

root = tk.Tk()

# setting the windows size
root.geometry("600x400")

# declaring string variable
# for storing name and Tpassword
name_var = tk.StringVar()
birthdate_var = tk.StringVar()
gender_var = tk.StringVar()
tree = None

def item_selected(event, tree):
   for selected_item in tree.selection():
      item = tree.item(selected_item)
      record = item['values']
      # show a message
      showinfo(title='Information', message=','.join(record))


def selektcxelo(event, tree):
   values = []
   zono = tree.identify("region", event.x, event.y)
   lakolumno = int(tree.identify_column(event.x)[1:])
   if zono == 'heading':
      print('head ' + str(lakolumno))
      print(tree.get_children())
      for line in tree.get_children():
         print(tree.item(line))
         print(tree.item(line)['values'][lakolumno - 1])
         values.append(tree.item(line)['values'])
      sorted_values = sorted(values, key=lambda x: (x[lakolumno - 1] == "", x[lakolumno - 1].lower()))
      tree.delete(*tree.get_children())
      for value in sorted_values:
         contact=(value[0], value[1], value[2])
         tree.insert('', tk.END, values=contact)


   else:
      print('not a head')
      return None


def create_tree_widget(frame):
   columns = ('name', 'birthdate', 'gender')
   tree = ttk.Treeview(frame, columns=columns, show='headings')
   tree.bind('<Button>', lambda event: selektcxelo(event, tree))


   # define headings
   tree.heading('name', text='Name')
   tree.heading('birthdate', text='Birthdate')
   tree.heading('gender', text='Gender')

   tree.bind('<<TreeviewSelect>>', lambda event: item_selected(event, tree))
   tree.grid(row=0, column=0, sticky=NSEW)

   # add a scrollbar
   scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
   tree.configure(yscroll=scrollbar.set)
   scrollbar.grid(row=0, column=1, sticky='ns')

   # generate sample data
   # contacts = []

   # for n in range(1, 100):
   #     contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

   # add data to the treeview
   # for contact in contacts:
   #     tree.insert('', tk.END, values=contact)

   return tree


# def item_selected(self, event):
#    for selected_item in self.tree.selection():
#       item = self.tree.item(selected_item)
#       record = item['values']
#       # show a message
#       showinfo(title='Information', message=','.join(record))

# defining a function that will
# get the name and password and
# print them on the screen
def add_a_player():
    name = name_var.get()
    birthdate = birthdate_var.get()
    gender = gender_var.get()

    print("The name is : " + name)
    print("The birthdate is : " + birthdate)
    print("The gender is : " + gender)

    contact = (name, birthdate, gender)
    tree.insert('', tk.END, values=contact)
    name_var.set("")
    birthdate_var.set("")
    gender_var.set("")



# creating a label for
# name using widget Label
tree_frame = LabelFrame(root, text='Players list')
tree_frame.pack()
tree = create_tree_widget(tree_frame)

action_frame = LabelFrame(root, text='Actions')
action_frame.pack()

load_btn = Button(action_frame, text='Load', command=lambda: print('Not implemented'))
load_btn.grid(row=0, column=0, padx=10, pady=10)
save_btn = Button(action_frame, text='Save', command=lambda: print('Not implemented'))
save_btn.grid(row=0, column=1, padx=10, pady=10)
close_btn = Button(action_frame, text='Close', command=lambda: print('Not implemented'))
close_btn.grid(row=0, column=2, padx=10, pady=10)

form_frame = LabelFrame(root, text='Player')
form_frame.pack()



name_label = Label(form_frame, text='Username', font=('calibre', 10, 'bold'))

# creating a entry for input
# name using widget Entry
name_entry = Entry(form_frame, textvariable=name_var, font=('calibre', 10, 'normal'))

# creating a label for password
birthdate_label = Label(form_frame, text='Birthdate', font=('calibre', 10, 'bold'))

# creating a entry for password
birthdate_entry = DateEntry(form_frame, textvariable=birthdate_var, date_pattern='dd/mm/yyyy')
birthdate_entry.delete(0, END)

gender_label = Label(form_frame, text='Gender', font=('calibre', 10, 'bold'))

gender_entry = Spinbox(form_frame, values=('', 'Male', 'Female'), textvariable=gender_var)
# creating a button using the widget
# Button that will call the add function
sub_btn = Button(form_frame, text='Add', command=add_a_player)

# placing the label and entry in
# the required position using grid
# method
name_label.grid(row=0, column=0)
name_entry.grid(row=1, column=0)
birthdate_label.grid(row=0, column=1)
birthdate_entry.grid(row=1, column=1)
gender_label.grid(row=0, column=2)
gender_entry.grid(row=1, column=2)
sub_btn.grid(row=2, column=0)

# performing an infinite loop
# for the window to display
root.mainloop()
