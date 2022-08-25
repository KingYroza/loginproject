import hashlib

PASSWORD_SALT = "3e0153433be7b9b9ec2e377c275f9caa0ed99c13902347a12c9227af19609894"

PASSWORD_USER = "qwerty123456"

SHA = hashlib.sha256((PASSWORD_USER + PASSWORD_SALT).encode()).hexdigest()

print(SHA)