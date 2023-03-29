import customtkinter
from passworManager import PasswordManager
from user import User
from databaseManager import DatabaseManager

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("520x530")
app.resizable(False, False)

user = User()
AccountDb = DatabaseManager()

##################################################################################################
#                                         Register View                                          #
##################################################################################################
def register_view():
    app.title("Add Password")

    
    def button_callback():
        print("Adding Note:", note_entry.get())
        print("Adding Username:", entry_1.get())
        print("Adding Password:", entry_2.get())
        if entry_2.get() == entry_3.get():
            AccountDb.create_main_account(entry_1.get(), entry_2.get(), note_entry.get())
            frame_1.destroy()
            main()
        
        
    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="Create your account")
    label_1.pack(pady=10, padx=10)

    note_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text="hint")
    note_entry.pack(pady=10, padx=10)

    entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="email or username")
    entry_1.pack(pady=10, padx=10)

    entry_2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="password", show="*")
    entry_2.pack(pady=10, padx=10)
    
    entry_3 = customtkinter.CTkEntry(master=frame_1, placeholder_text="retype password", show="*")
    entry_3.pack(pady=10, padx=10)

    button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text="Create Account")
    button_1.pack(pady=10, padx=10)

    app.mainloop()

##################################################################################################
#                                            Login View                                          #
##################################################################################################
def main():
    app.title("Login")
    
    if AccountDb.check_for_main_account() == False:
        print("No main account found, creating one.")
        register_view()
        
    
    def button_callback():
        print("validating username:", entry_1.get())
        print("validating Password:", entry_2.get())
        if AccountDb.authenticate_main_account(entry_1.get(), entry_2.get()):
            PasswordManager.createFernet(entry_1.get(), entry_2.get())
            user.username = entry_1.get()
            user.password = entry_2.get()
            print("Login Successful")
            frame_1.destroy()
            home_view()
        else:
            label_1.configure(text="Invalid username or password")
            entry_1.delete(0, "end")
            entry_2.delete(0, "end")
            entry_1.focus()
    
    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="One Password to rule them all.")
    label_1.pack(pady=10, padx=10)

    entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="email or username")
    entry_1.pack(pady=10, padx=10)

    entry_2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="password", show="*")
    entry_2.pack(pady=10, padx=10)

    button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text="Login")
    button_1.pack(pady=10, padx=10)

    app.mainloop()

##################################################################################################
#                                 Home View (after login)                                        #
##################################################################################################
def home_view():
    app.title("Home")
    
    def back_click():
        home_frame.destroy()
        main()
    
    def add_password_click():
        home_frame.destroy()
        add_password_view() 
        
    def search_click():
        print("Searching for:", entry_1.get())
    
    home_frame = customtkinter.CTkFrame(master=app)
    home_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    back_btn = customtkinter.CTkButton(master=home_frame, text="Logout", command=back_click)
    back_btn.grid(row=0, column=0, padx=10, pady=10)
    
    add_password_btn = customtkinter.CTkButton(master=home_frame, text="Add Account", command=add_password_click)
    add_password_btn.grid(row=0, column=2, padx=10, pady=10)
    
    entry_1 = customtkinter.CTkEntry(master=home_frame, placeholder_text="Search Accounts")
    entry_1.grid(row=1, column=1, padx=10, pady=10)
    
    view_passwords_btn = customtkinter.CTkButton(master=home_frame, text="Search", command=search_click)
    view_passwords_btn.grid(row=2, column=1, padx=10, pady=10)
    
    scroll_frame = customtkinter.CTkScrollableFrame(master=home_frame, label_text="Accounts", width=400, height=250)
    scroll_frame.grid(row=3, column=0, columnspan=3, pady=10)
    scroll_items = []
    accounts = AccountDb.get_all_accounts()
    for a in accounts:
        # drop down menu
        account_combo = customtkinter.CTkComboBox(scroll_frame, values=["Note: " + a["note"], "Username: " + a["username"], "Password: " + a["password"].decode()], width=350, height=30)
        account_combo.pack(pady=10, padx=10)
        scroll_items.append(account_combo)
    
    app.mainloop()


##################################################################################################
#                                            Add Password View                                   #
##################################################################################################
def add_password_view():
    app.title("Add Password")
    
    def back_click():
        frame_1.destroy()
        home_view()
    
    def button_callback():
        print("Adding Note:", note_entry.get())
        print("Adding Username:", entry_1.get())
        
        plain_password = entry_2.get()
        AccountDb.add_account(note_entry.get(), entry_1.get(), plain_password, 'www.google.com')
        print("Adding Password:", entry_2.get())
        back_click()
        
    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    back_btn = customtkinter.CTkButton(master=frame_1, text="Back", command=back_click)
    back_btn.pack(padx=10, pady=10)

    label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="Add a New Account")
    label_1.pack(pady=10, padx=10)

    note_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text="note")
    note_entry.pack(pady=10, padx=10)

    entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="email or username")
    entry_1.pack(pady=10, padx=10)

    entry_2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="password", show="*")
    entry_2.pack(pady=10, padx=10)

    button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text="Add")
    button_1.pack(pady=10, padx=10)

    app.mainloop()
    
    
##################################################################################################
#                                           Main                                                 #
##################################################################################################
if __name__ == "__main__":
    main()