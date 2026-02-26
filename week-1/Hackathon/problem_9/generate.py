
from cryptography.fernet import Fernet

key = Fernet.generate_key()
open("secret.key", "wb").write(key)
