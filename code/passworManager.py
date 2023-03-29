###################################################################################################
#     this class handles hashing and salting passwords, and checking passwords against hashes
#     it also handles the encryption and decryption of passwords
#     it also stores the passwords in a file
###################################################################################################
import hashlib
import settings
from cryptography.fernet import Fernet
import os
import base64

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

def get_fernet_key(hashed_key):
    # encode the hashed key using base64
    fernet_key = base64.urlsafe_b64encode(hashed_key.encode()[:32])
    # return the Fernet key
    return fernet_key

class PasswordManager:
    f = None
    def createFernet(username, password):
        #hash the secret key with the username and password
        combinedKey = username.encode() + password.encode()
        hashedKey = hashlib.sha256(combinedKey).hexdigest()
        fernet_key = get_fernet_key(hashedKey)
        PasswordManager.f = Fernet(fernet_key)

    def hashPassword(password):
        hashedKey = hashlib.sha256(password.encode()).hexdigest()
        return hashedKey

    def checkPassword(password, hashed_password):
        if PasswordManager.hashPassword(password) == hashed_password:
            return True
        else:
            return False
    
    def encryptPassword(password):
        # encrypt password using Fernet
        encrypted_password = PasswordManager.f.encrypt(password.encode())
        return encrypted_password
    
    # def addPassword(plain_password):
    #     hashed_password = PasswordManager.encryptPassword(plain_password)
    #     # add password to file
    #     with open("passwords.txt", "a") as file:
    #         file.write(hashed_password.decode() + "\n")
    #     file.close()
        
    def decryptPassword(encrypted_password):
        # decrypt the password
        decrypted_password = PasswordManager.f.decrypt(encrypted_password)
        return decrypted_password
    
    # def getPasswords():
    #     # get passwords from file
    #     with open("passwords.txt", "r") as file:
    #         passwords = file.readlines()
    #     file.close()
    #     decryptedPasswords = []
    #     for p in passwords:
    #         # strip newline from password
    #         p = p.strip()
    #         decrypted_password = PasswordManager.decryptPassword(p.encode())
    #         decryptedPasswords.append(decrypted_password)
    #     return decryptedPasswords
            