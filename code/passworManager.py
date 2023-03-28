###################################################################################################
#     this class handles hashing and salting passwords, and checking passwords against hashes
#     it also handles the encryption and decryption of passwords
#     it also stores the passwords in a file
###################################################################################################
import hashlib
import settings

secretKey = settings.SECRET_KEY


class PasswordManager:
    def encryptPassword(password):
        # encrypt password using sha256 with a secret key
        hashedPassword = hashlib.sha256(password.encode() + secretKey.encode()).hexdigest()
        return hashedPassword
    
    def addPassword(plain_password):
        hashed_password = PasswordManager.encryptPassword(plain_password)
        # add password to file
        with open("passwords.txt", "a") as file:
            file.write(hashed_password + "")
        file.close()
            