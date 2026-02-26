from cryptography.fernet import Fernet

key = open("secret.key", "rb").read()
f = Fernet(key)

encrypted = open("input.txt.encrypted", "rb").read()
decrypted = f.decrypt(encrypted)
open("input.txt.decrypted", "wb").write(decrypted)
