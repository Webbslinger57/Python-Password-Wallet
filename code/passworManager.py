###################################################################################################
#     this class handles hashing and salting passwords, and checking passwords against hashes
#     it also handles the encryption and decryption of passwords
#     it also stores the passwords in a file
###################################################################################################
import hashlib
import settings
from cryptography.fernet import Fernet
import os

KEY_FILE = 'secret.key'

def loadKey():
    # check if the key file exists
    if os.path.exists(KEY_FILE):
        # load the key from the file
        with open(KEY_FILE, 'rb') as f:
            secretKey = f.read()
    else:
        # generate a new key
        secretKey = Fernet.generate_key()
        # save the key to the file
        with open(KEY_FILE, 'wb') as f:
            f.write(secretKey)
    return secretKey

# load or generate the secret key
secretKey = loadKey()

# create a Fernet object with the secret key
f = Fernet(secretKey)

class PasswordManager:
    def encryptPassword(password):
        # encrypt password using Fernet
        encrypted_password = f.encrypt(password.encode())
        return encrypted_password
    
    def addPassword(plain_password):
        hashed_password = PasswordManager.encryptPassword(plain_password)
        # add password to file
        with open("passwords.txt", "a") as file:
            file.write(hashed_password.decode() + "\n")
        file.close()
        
    def decryptPassword(encrypted_password):
        # decrypt the password
        decrypted_password = f.decrypt(encrypted_password).decode()
        return decrypted_password
    
    def getPasswords():
        # get passwords from file
        with open("passwords.txt", "r") as file:
            passwords = file.readlines()
        file.close()
        decryptedPasswords = []
        for p in passwords:
            # strip newline from password
            p = p.strip()
            decrypted_password = PasswordManager.decryptPassword(p.encode())
            decryptedPasswords.append(decrypted_password)
        return decryptedPasswords
            