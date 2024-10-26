# ============================== SETUPS ============================== 


import back
from tkinter import *
from tkinter import messagebox
from customtkinter import *
from CTkListbox import *
from CTkTable import *
from khayyam import *



window = CTk()
window.title("hey")
window.geometry('575x400')

def clear_list():
    listOfItems.delete(0,END)


# ============================== TITLES ============================== 


fullnameLabel = CTkLabel(window, text="Full Name")
fullnameLabel.grid(row=0, column=0, pady= 10)

birthdayLabel = CTkLabel(window, text="birthday")
birthdayLabel.grid(row=0, column=2, pady=10, padx=15)

phoneLabel = CTkLabel(window, text="Phone")
phoneLabel.grid(row=1, column=0)

locationLabel = CTkLabel(window, text="Location")
locationLabel.grid(row=1, column=2)


# ============================== ENTRIES ============================== 


fullnameText = StringVar()                    # inserting full name
fullnameEntry = CTkEntry(window, textvariable=fullnameText)
fullnameEntry.grid(row=0, column=1)

birthdayText = StringVar()                    # inserting birthday
birthdayEntry = CTkEntry(window,textvariable=birthdayText)
birthdayEntry.grid(row=0, column=3)

phoneText = StringVar()                    # inserting phone
phoneEntry = CTkEntry(window, textvariable=phoneText)
phoneEntry.grid(row=1, column=1)

locationText = StringVar()                    # inserting location
locationEntry = CTkEntry(window, textvariable=locationText)
locationEntry.grid(row=1, column=3)


# ============================== THE LIST ============================== 


listOfItems = CTkListbox(window, width=300, height=250)             # the actual list
listOfItems.grid(row=3, column=0, rowspan=6, columnspan=2, padx=10) 


def get_selected_row(event):
    global selected
    index = listOfItems.curselection()
    selected = listOfItems.get(index)

    fullnameEntry.delete(0, END)
    fullnameEntry.insert(END, selected[1])

    birthdayEntry.delete(0, END)
    birthdayEntry.insert(END, selected[2])

    phoneEntry.delete(0, END)
    phoneEntry.insert(END, selected[3])

    locationEntry.delete(0, END)
    locationEntry.insert(END, selected[4])


listOfItems.bind("<<ListboxSelect>>", get_selected_row)


# ============================== BUTTONS & THEIR ACTIONS ============================== 


def view_items():          # displays all the items in the list
    clear_list()
    people = back.view()
    for person in people:
        listOfItems.insert(END, person)    

viewButton = CTkButton(window, text="View All", width=150, command= view_items)  # triggers the displaying function
viewButton.grid(row=3, column=2, columnspan=2)


def add_item():       # adds the inserted item to the list
    if fullnameText.get() == "" or birthdayText.get() == "" or phoneText.get() == "" or locationText.get() == "":    # check if the user has not entered anything
        messbirthdaybox.showwarning("Empty Fields", "Please fill up all the boxes.")
    else:
        back.insert(fullnameText.get(), birthdayText.get(), phoneText.get(), locationText.get())
        fullnameEntry.delete(0, END)
        birthdayEntry.delete(0, END)
        phoneEntry.delete(0, END)
        locationEntry.delete(0, END)
    view_items()

addButton = CTkButton(window, text="Add +", width=150, command= add_item) # triggers the adding function
addButton.grid(row=4, column=2, columnspan=2)


def edit_item():
    back.edit(selected[0], fullnameText.get(), birthdayText.get(), phoneText.get(), locationText.get())
    fullnameEntry.delete(0, END)
    birthdayEntry.delete(0, END)
    phoneEntry.delete(0, END)
    locationEntry.delete(0, END)
    view_items()


editButton = CTkButton(window, text="Edit", width=150, command=edit_item)
editButton.grid(row=5, column=2, columnspan=2)

def remove_item():
    back.remove(selected[0])
    fullnameEntry.delete(0, END)
    birthdayEntry.delete(0, END)
    phoneEntry.delete(0, END)
    locationEntry.delete(0, END)
    view_items()

removeButton = CTkButton(window, text="Remove -", width=150, command=remove_item)
removeButton.grid(row=6, column=2, columnspan=2)


# ============================== SEARCH BOX ============================== 

def search_items():
    clear_list()
    people = back.search(searchText.get())
    for person in people:
        listOfItems.insert(END, person)


searchButton = CTkButton(window, text="Search", command= search_items)
searchButton.grid(row=2, column=0, padx=5, pady=10)

searchText = StringVar()                    # inserting item to search
searchEntry = CTkEntry(window, textvariable=searchText)
searchEntry.grid(row=2, column=1)


# ============================== CONNECT WITH BACKEND ============================== 



    
view_items()





window.mainloop()



# ============================== COMMENT ============================== 







# current = JalaliDate.today()
# print(f"age:{current.year - int(birthdayText.split()[0]) - ((current.month, current.day) < (int(birthdayText.spl[1]), int(birthday[2])))}")