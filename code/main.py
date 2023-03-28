import customtkinter
from passworManager import PasswordManager

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("500x400")
app.resizable(False, False)


##################################################################################################
#                                            Login View                                          #
##################################################################################################
def main():
    app.title("Login")
    
    def button_callback():
        print("validating username:", entry_1.get())
        print("validating Password:", entry_2.get())
        if entry_1.get() == "admin" and entry_2.get() == "admin":
            print("Login Successful")
            frame_1.destroy()
            home_view()
    
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
    
    def add_password_click():
        home_frame.destroy()
        add_password_view() 
        
    def view_passwords_click():
        print("Viewing Passwords")
    
    home_frame = customtkinter.CTkFrame(master=app)
    home_frame.pack(pady=20, padx=60, fill="both", expand=True)
    
    add_password_btn = customtkinter.CTkButton(master=home_frame, text="Add Password", command=add_password_click)
    add_password_btn.pack(pady=10, padx=10)
    
    view_passwords_btn = customtkinter.CTkButton(master=home_frame, text="View Passwords", command=view_passwords_click)
    view_passwords_btn.pack(pady=10, padx=10)


##################################################################################################
#                                            Add Password View                                   #
##################################################################################################
def add_password_view():
    app.title("Add Password")
    
    def button_callback():
        print("Adding Note:", note_entry.get())
        print("Adding Username:", entry_1.get())
        
        plain_password = entry_2.get()
        PasswordManager.addPassword(str(plain_password))
        print("Adding Password:", entry_2.get())
        
    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT)
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