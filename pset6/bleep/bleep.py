from cs50 import get_string
from sys import argv


def main():
    
    # check number of arguments is correct
    if len(argv) != 2:
        print('Usage: python bleep.py dictionary')
        exit()
        
    else:
        filename = argv[1]
        
        with open(filename, 'r') as f:
            banned_words = f.readlines()
        
        # strip newline characters from words in list
        banned_words = [w.strip('\n') for w in banned_words]
        
        uncensored = input("What would you like to censor?\n")
        uncensored_words = uncensored.split()
        censored_words = []
        
        # check if each word is in the banned list
        for word in uncensored_words:
            len_word = len(word)
            if word.lower() in banned_words:
                word = len_word*'*'
            censored_words.append(word)
        
        censored = ' '.join(censored_words)
        print(censored)

if __name__ == "__main__":
    main()
