from passworManager import PasswordManager
import sqlite3
import uuid

class DatabaseManager:
    conn = None
    c = None
    
    def __init__(self):
        self.conn = sqlite3.connect('accounts.db') 
        self.c = self.conn.cursor()

        self.c.execute('''
                CREATE TABLE IF NOT EXISTS Accounts
                ([account_id] INTEGER PRIMARY KEY, [notes] TEXT, [username] TEXT, [password] TEXT, [url] TEXT)
                ''')
        self.c.execute('''
                CREATE TABLE IF NOT EXISTS MainAccount
                ([account_id] INTEGER PRIMARY KEY,[username] TEXT, [password] TEXT, [hint] TEXT)
                       ''')
        
        self.conn.commit()  
        
    def check_for_main_account(self):
        main_account = self.c.execute("SELECT * FROM MainAccount").fetchone()
        if main_account is None:
            print(main_account)
            return False
        else:
            print("Main account found.")
            return True  
    
    def authenticate_main_account(self, p_username, p_password):
        if self.c.execute("SELECT * FROM MainAccount"):
            account_info = self.c.execute("SELECT * FROM MainAccount").fetchone()
            username, hashed_password = account_info[1], account_info[2]
            print(PasswordManager.checkPassword(p_password, hashed_password))
            if PasswordManager.checkPassword(p_password, hashed_password):
                print("Main account authenticated.")
                return True
        else:
            return False
        
    def create_main_account(self, username, password, hint):
        hashed_password = PasswordManager.hashPassword(password)
        self.c.execute("INSERT INTO MainAccount (username, password, hint) VALUES (?, ?, ?)", (username, hashed_password, hint))
        self.conn.commit()
        print("Main account created.")

    def add_account(self, note, username, password, url):
        encrypted_password = PasswordManager.encryptPassword(password)
        self.c.execute("INSERT INTO Accounts (notes, username, password, url) VALUES (?, ?, ?, ?)", (note, username, encrypted_password, url))
        self.conn.commit()
        
    def get_account(self, id):
        self.c.execute("SELECT * FROM Accounts WHERE account_id = ?", (id,))
        return self.c.fetchone()

    def get_all_accounts(self):
        self.c.execute("SELECT * FROM Accounts")
        accounts = []
        for row in self.c.fetchall():
            account = {"id": row[0], "note": row[1], "username": row[2], "password": PasswordManager.decryptPassword(row[3]), "url": row[4]}
            accounts.append(account)
        return accounts