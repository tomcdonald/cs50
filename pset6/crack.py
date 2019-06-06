import sys
from itertools import product
from string import ascii_letters
from crypt import crypt

def main():
    if len(sys.argv) != 2:
        print('Usage: python crack.py hashed_password')
        exit()
    else:
        hashed_password = sys.argv[1]
    crack(hashed_password)
    
def crack(hashed_password):
    salt = hashed_password[:2]
    for num_letters in range(1, 6):
        passwords = (''.join(i) for i in product(ascii_letters, 
                                                 repeat = num_letters))
        for password in passwords:
            encrypted_password = crypt(password, salt)
            if encrypted_password == hashed_password:
                print(password)
                exit()

if __name__ == '__main__':
    main()