#This program creates a password save file

#Date Created: 3/24/2025
#Creator: ElectrifyThunder

#Services
import tkinter as tk
import time
from tkinter import Frame,Entry,Label,Checkbutton,Button,Scrollbar,Canvas,BooleanVar #Confirmed Labels I'll be using today.
from tkinter import messagebox

accounts = "accounts.txt" #save data file
root = tk.Tk() #main program

class updateAccount(): #accountClass
    def __init__(self,username,password,favorite,root):
        self.username = username
        self.password = password
        self.favorite = favorite
        self.currentRoot = root

    def getUsername(self):
        return self.username
    def getPassword(self):
        return self.password
    def getFavorite(self):
        return self.favorite
    def getMainRoot(self):
        return self.currentRoot
    
    def setFavorite(self,fav):
        self.favorite = fav
    def setUsername(self,username):
        self.username = username
    def setPassword(self,password):
        self.password = password
    def setMainRoot(self,root):
        self.currentRoot = root

updateAccount.setFavorite(updateAccount,False)

def submitAccount(event,myuser,mypass,myPlatform): #User submits new written data
    myuserText = myuser.get()
    mypassText = mypass.get()
    myPlatformText = myPlatform.get()

    updateAccount.getMainRoot(updateAccount).destroy()

    if myuserText != "" and mypassText != "" and myPlatformText != "":
        if updateAccount.getFavorite(updateAccount):
            accounts = "favorites.txt"
        else:
            accounts = "Accounts.txt"

        with open(accounts,"a") as file:
            file.write(f"\n Platform : {myPlatformText} Username : {myuserText} Password : {mypassText} ")
        
        loadAccounts(False) #Reload the data to update the frame
    else:
        messagebox.showerror("Cannot be Empty.","More than one entrybox is empty!")
        
def userEntrySave(event,myEntry): #User enters a new data entry
    text = event.widget
    labelName = event.widget._name
    setText = text.get()

    if labelName == "password":
        updateAccount.setPassword(updateAccount,setText)
    elif labelName == "username":
        updateAccount.setUsername(updateAccount,setText)

def focusedInText(event,myEntry): #User focuses into the chat
    text = event.widget
    if text != "":
        myEntry.delete(0,tk.END)

def closeWindow(event):
    getWindow = updateAccount.getMainRoot(updateAccount)
    if getWindow:
        getWindow.destroy()

dockFrame = Frame(root, bg="grey")

allLogins = Button(dockFrame, height=2,width=22,text="All Items",font="Terminator")
allLogins.pack()

favorites = Button(dockFrame, height=2,width=22,text="⭐Favorites",font="Terminator")
favorites.pack()

trash = Button(dockFrame, height=2,width=22,text="Trash",font="Terminator")
trash.pack()

newAccount = Button(dockFrame, height=2,width=22,text="New Account",font="Terminator")
newAccount.pack()

dockFrame.pack(fill="y", side="left")

topBar = Frame(root, bg="blue",height=25)
topBar.pack(fill="x", side="top")

exitButton = tk.Button(topBar,bg="red")
exitButton.bind("<ButtonPress>",closeWindow)
exitButton.pack(fill="x",side="left")

# Create a frame for the scrollbar
scroll_frame = Frame(root)
scroll_frame.pack(fill="both", expand=True)

# Create a canvas widget
canvas = Canvas(scroll_frame)
canvas.pack(side="left", fill="both", expand=True)

# Add a vertical scrollbar to the frame
scrollbar = Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas
myAccounts = Frame(canvas)

# Add the new frame to a window in the canvas
canvas.create_window((0, 0), window=myAccounts, anchor="nw")

def accountHover(theLabel:Label,Action:str):
    if Action == "Enter":
        theLabel.config(bg="red")
    elif Action == "Leave":
        theLabel.config(bg="grey")

def addToFavorites(theLabel: Label):
    getText = theLabel.cget("text").split("Username: ")[1].strip()
    myUser = None
    myPass = None
    myPlatform = None

    with open(accounts, "r") as file:
        myLines = file.readlines()

        usernames = []
        passwords = []
        platforms = []
        
        for line in myLines:
            if "Username" in line and "Password" in line and "Platform" in line:
                username = line.split("Username :")[1].split("Password")[0].strip()
                password = line.split("Password :")[1].split("Platform")[0].strip()
                platform = line.split("Platform :")[1].strip()

                myUser = username
                myPass = password
                myPlatform = platform

                usernames.append(username)
                passwords.append(password)
                platforms.append(platform)
        
        filteredLines = [line for line in myLines if getText not in line]

        if getText in [username.strip() for username in usernames]:
            print("Username found in the list")

            with open(accounts,"w") as file:
                file.writelines(filteredLines)
            
            with open("favorites.txt","w") as file:
                file.writelines(f"Username : {myUser} Password : {myPass} Platform : {myPlatform}")

            loadAccounts("accounts")

        else:
            print("Username not found in the list")
        
def loadAccounts(whatLoading):
    if whatLoading == "accounts":
        accounts = "accounts.txt"
    elif whatLoading == "favorites":
        accounts = "favorites.txt"
    elif whatLoading == "trash":
        accounts = "trash.txt"

    for widget in myAccounts.winfo_children():
        widget.destroy()  # Deletes old data so it won't copy and paste

    with open(accounts, "r") as file:  # Update new data
        myLines = file.readlines()
        usernames = [line.split("Username :")[1].split("Password")[0].strip() for line in myLines if "Username" in line]
        passwords = [line.split("Password :")[1].split("Username")[0].strip() for line in myLines if "Username" in line]
        platforms = [line.split("Platform :")[1].split("Username")[0].strip() for line in myLines if "Username" in line]

    for i, (user, passwd, pltform) in enumerate(zip(usernames, passwords, platforms)):
        base_row = i * 4  # Each set of labels will take up 4 rows
        column = 0  # All labels will be in the same column
        
        username_label = Label(myAccounts, text=f"Username: {user} ", bg="grey", font="Terminator")
        username_label.grid(row=base_row, column=column, pady=(10, 0))  # Add padding to space out the labels
        
        username_label.bind("<Button-1>", lambda event, myLabel=username_label: addToFavorites(myLabel))
        username_label.bind("<Enter>", lambda event, myLabel=username_label: accountHover(myLabel, "Enter"))
        username_label.bind("<Leave>", lambda event, myLabel=username_label: accountHover(myLabel, "Leave"))

        password_label = Label(myAccounts, text=f"Password: {passwd}", bg="grey", font="Terminator")
        password_label.grid(row=base_row + 1, column=column, pady=(5, 0))  # Add padding to space out the labels

        platform_label = Label(myAccounts, text=f"Platform: {pltform}", bg="grey", font="Terminator")
        platform_label.grid(row=base_row + 2, column=column, pady=(5, 10))  # Add padding to space out the labels
        
def checkbox_changed(event,checkVar,checkLabel:Label): #Checks if checkbox has been changed.
    current_value = checkVar.get()
    new_value = 0 if current_value == 1 else 1
    checkVar.set(new_value)
    if new_value == 1:
        updateAccount.setFavorite(updateAccount,True)
        checkLabel.config(text="Favorited")
    else:
        updateAccount.setFavorite(updateAccount,False)
        checkLabel.config(text="UnFavorited")

def createNewAccount():
    openRoot = tk.Tk()
    openRoot.title("Create new account")
    openRoot.geometry("800x600")

    updateAccount.setMainRoot(updateAccount,openRoot)

    #User enters the desired entries here
    enterPlatform = Label(openRoot,name="platformlabel",text="Plaform:")
    enterPlatform.pack()

    platformEntry = Entry(openRoot,name="platform")
    platformEntry.bind("<Return>",lambda event, userEntry=platformEntry:userEntrySave(event,userEntry))
    platformEntry.pack()

    enterUsername = Label(openRoot,name="userLabel",text="Username:")
    enterUsername.pack()

    userEntry = Entry(openRoot,name="username")
    userEntry.bind("<Return>",lambda event, userEntry=userEntry:userEntrySave(event,userEntry))
    userEntry.pack()

    enterPassword = Label(openRoot,name="passlabel",text="Password:")
    enterPassword.pack()

    passEntry = Entry(openRoot,name="password",show="*")
    passEntry.bind("<Return>",lambda event, passEntry=passEntry:userEntrySave(event,passEntry))
    passEntry.pack()

    #User submits the account here
    submit = Button(openRoot,text="SUBMIT")
    submit.bind("<ButtonRelease>",lambda event, username=userEntry,userPass=passEntry,platform=platformEntry:submitAccount(event,userEntry,passEntry,platform))
    submit.pack()

    checkbox_var = tk.IntVar(value=0)

    checkBox = Checkbutton(
        openRoot,
        text="UnFavorited",
        variable=checkbox_var,
        font="Terminator",
        indicatoron=False,
        bg="Lightgray",
        fg="black",
        activebackground="darkgray",
        activeforeground="white",
        relief="raised",
        bd=2
    )

    checkBox.bind("<ButtonPress>",lambda event,checkBox=checkBox:checkbox_changed(event,checkbox_var,checkBox))
    checkBox.pack()

    openRoot.mainloop()

loadAccounts("accounts") #Load the account data

allLogins.bind("<ButtonRelease>",lambda event,whatLoading="accounts":loadAccounts(whatLoading))
favorites.bind("<ButtonRelease>",lambda event,whatLoading="favorites":loadAccounts(whatLoading))
trash.bind("<ButtonRelease>",lambda event, whatLoading="trash":loadAccounts(whatLoading))


newAccount.bind("<ButtonRelease>",lambda event:createNewAccount())

root.title("Account Manager")
root.geometry("800x600")

updateAccount.setMainRoot(updateAccount,root)

root.mainloop()