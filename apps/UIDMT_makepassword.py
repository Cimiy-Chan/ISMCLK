"""
This small apps is used to make the token of password and
store in the user_registration.db
"""

import abc
from cryptography.fernet import Fernet

# Below is the private key. This is used to generate the public as per your password input
# Don't change this key.
private_key = 'IxkXNINr4ZAAsEIYJUpeUe51fP0HNT54SabeEq2KRiA='

f = Fernet(private_key)

password_input = input('Please input your password: ')
token = f.encrypt(bytes(password_input, 'UTF-8'))


print(f'Hashed_pwd = {token.decode()}')
print('\n\nPlease select it and use ctrl-c/ctrl-v for copy and paste the hashed pwd')

# Verification
verf_pw = bytes.decode(Fernet(private_key).decrypt(token), 'UTF-8')

if verf_pw == password_input:
    print('Verification OK...')
else:
    print('Wrong token...')
