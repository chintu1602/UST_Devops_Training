from cryptography.fernet import Fernet

key = open("secret.key", "rb").read()
f = Fernet(key)

data = open("input.txt", "rb").read()
encrypted = f.encrypt(data)
open("input.txt.encrypted", "wb").write(encrypted)



